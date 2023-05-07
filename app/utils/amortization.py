import numpy as np
import pandas as pd
import numpy_financial as npf
from scipy.optimize import minimize, Bounds
import copy


class Amortization:
    """
    Get the amortization table of a loan for a client or simple financial modelling.

    Attributes
    ----------
    amount : float
        loan's amount
    rate : float
        interest rate with capitalization for each time period
    t : int
        number of periods the loan will last for
    default_prob : float
        probability of a client defaulting, default 0.2

    Methods
    -------
    payment_amount : float
        annuity of the loan considering interest rate and time
    client_dataframe : pd.DataFrame
        a client-friendly amortization table
    financial_dataframe : pd.DataFrame
        with extra financial information relevant to our models
    expected_irr : float
        expected IRR of the loan project
    """

    def __init__(self, amount: float, rate: float, t: int, default_prob: float = 0.2):
        self.amount = amount
        self.rate = rate
        self.t = t
        self.default_prob = default_prob

    @property
    def payment_amount(self) -> float:
        return self.amount * self.rate / (1 - (1 + self.rate) ** (-self.t))

    def client_dataframe(self) -> pd.DataFrame:
        times = list(range(1, self.t + 1))
        payments = [self.payment_amount for _ in range(self.t)]

        initial_interest = self.amount * self.rate
        initial_principal = self.payment_amount - initial_interest
        balances = [self.amount]
        interests = [initial_interest]
        principals = [initial_principal]
        new_balances = [self.amount - initial_principal]

        for _ in times[1:]:
            balances.append(new_balances[-1])
            interests.append(balances[-1] * self.rate)
            principals.append(self.payment_amount - interests[-1])
            new_balances.append(balances[-1] - principals[-1])

        df = pd.DataFrame.from_dict({
            "T": times,
            "Balance": balances,
            "Payment": payments,
            "Interest": interests,
            "Principal": principals,
            "New Balance": new_balances
        }).set_index("T")
        return df

    def financial_dataframe(self) -> pd.DataFrame:
        # Completed
        times = list(range(0, self.t + 1))
        payments = [0.] + [self.payment_amount for _ in range(self.t)]
        balances = [self.amount]
        interests = [0]
        principals = [0]
        cashflows = [-self.amount]
        irr = [0]
        pds = [self.default_prob]

        for t in times[1:]:
            interest = balances[-1] * self.rate
            balances.append(balances[-1] - self.payment_amount + interest)
            interests.append(balances[-1] * self.rate)
            principals.append(self.payment_amount - interests[-1])
            cashflows.append(self.payment_amount)
            irr.append(npf.irr(cashflows))
            pds.append((1 - self.default_prob) ** t * self.default_prob)

        pds[-1] = (1 - self.default_prob) ** self.t
        expected_irr = np.array(pds) * np.array(irr)
        ead = np.array(balances) * np.array(pds) * np.array([0.75] * (self.t + 1))  # LGD is considered as 100%

        df = pd.DataFrame.from_dict({
            "T": times,
            "Balance": balances,
            "Payment": payments,
            "Interest": interests,
            "Principal": principals,
            "Cashflows": cashflows,
            "IRR": irr,
            "Default Prob": pds,
            "Expected IRR": expected_irr,
            "EAD": ead
        }).set_index("T")
        return df

    def expected_irr(self) -> float:
        cashflows = [-self.amount] + [self.payment_amount for _ in range(self.t)]

        irr = [0.] + [npf.irr(cashflows[:t + 1]) for t in range(1, self.t + 1)]
        pds = [(1 - self.default_prob) ** t * self.default_prob for t in range(self.t)] + [
            (1 - self.default_prob) ** self.t]

        return np.array(pds) @ np.array(irr)

    @staticmethod
    def optimize_expected_irr(target_rate: float, obj: 'Amortization') -> float:
        obj = copy.copy(obj)

        def e_irr(rate: np.array):
            obj.rate = rate[0]
            irr = obj.expected_irr()
            return (abs(irr) - target_rate) ** 2

        res = minimize(e_irr, [0.5], bounds=Bounds(0.001, ))
        return res.x[0]

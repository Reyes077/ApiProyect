from fastapi import FastAPI
from app.models.request_evaluation import RequestEvaluation
import pandas as pd
from app.utils.amortization import Amortization
from app.utils.load_ml_model import load_ml_model


model=load_ml_model("../app/Best_Model.pkl")

app = FastAPI()

@app.get("/health")
def health_check():
    return {"is_alive": True}

@app.post("/evaluate")
async def evaluate(req: RequestEvaluation):
    print(req)
    df = pd.DataFrame({
        'loan_amnt': [req.loan_amnt],
        'term': [req.term],
        'int_rate': [req.int_rate],
        'grade': [req.grade],
        'sub_grade': [req.sub_grade],
        'home_ownership': [req.home_ownership],
        'annual_inc': [req.annual_inc],
        'verification_status': [req.verification_status],
        'pymnt_plan': [req.pymnt_plan],
        'purpose': [req.purpose],
        'addr_state': [req.addr_state],
        'dti': [req.dti],
        'delinq_2yrs': [req.delinq_2yrs],
        'inq_last_6mths': [req.inq_last_6mths],
        'mths_since_last_delinq': [req.mths_since_last_delinq],
        'open_acc': [req.open_acc],
        'pub_rec': [req.pub_rec],
        'revol_util': [req.revol_util],
        'initial_list_status': [req.initial_list_status],
        'acc_now_delinq': [req.acc_now_delinq]
    })

    pred = model.predict_proba(df)[0]
    default_prob = pred[1]
    print(default_prob)
    amort = Amortization(100_000, 0.5, 12, default_prob)
    opt_rate = Amortization.optimize_expected_irr(0, amort)
    return {
        "pd": f"{default_prob * 100:.2}%",
        "interest_rate": f"{opt_rate * 100:.4f}%"
    }
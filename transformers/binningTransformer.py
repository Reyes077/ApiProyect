from typing import Dict, List
import pandas as pd


class BinningTransformer:
    def __init__(self, bins: Dict):
        self.bins = bins

    def __find_bin(self, value: float, mappings: List):
        for mapping in mappings:
            if value <= mapping["max"]:
                return mapping["label"]
        return "Error"

    def transform(self, X: pd.DataFrame, y: pd.DataFrame = None) -> pd.DataFrame:
        X = X.copy()
        for key in self.bins.keys():
            X.loc[:, key] = X.loc[:, key].transform(lambda x: self.__find_bin(x, self.bins[key]))
        return X

    def fit(self, *args, **kwargs):
        return self

    def __str__(self) -> str:
        return "BinningTransformer()"

    def __repr__(self) -> str:
        return "BinningTransformer()"
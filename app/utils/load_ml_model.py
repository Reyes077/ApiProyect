import pickle
from typing import Any


def load_ml_model(path: str) -> Any:
    link_model=path

    with open(link_model, "rb") as file:
        deserialized_model=pickle.load(file, fix_imports = True)

    return deserialized_model
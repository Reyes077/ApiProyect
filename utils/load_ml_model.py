import pickle
from typing import Any


def load_ml_model(path: str) -> Any:
    model_file=path

    with open(model_file, "rb") as file:
        deserialized_model=pickle.load(file, fix_imports = True)

    return deserialized_model
from utils import load_ml_model
import mlxtend

model = load_ml_model("./model.pkl")

print(model)
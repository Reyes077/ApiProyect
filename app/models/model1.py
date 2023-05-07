from xgboost.sklearn import XGBRegressor
from sklearn.model_selection import train_test_split
import pickle
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from app.models.bins import bins
from app.transformers import ColumnSelectorTransformer, BinningTransformer, WOETransformer
from sklearn.metrics import accuracy_score

df = pd.read_csv('./credit_risk_data_v2.csv')

cols_to_keep = ['loan_amnt', 'term', 'int_rate', 'grade', 'sub_grade', 'home_ownership', 'annual_inc',
                'verification_status', 'pymnt_plan', 'purpose', 'addr_state', 'dti', 'delinq_2yrs', 'inq_last_6mths',
                'mths_since_last_delinq', 'open_acc', 'pub_rec', 'revol_util', 'initial_list_status', 'acc_now_delinq']

seed = 0
##The best model in comparison models is xgbregresor with 95% accu
model = Pipeline([
    ('col selector', ColumnSelectorTransformer(columns=cols_to_keep)),
    ('bins', BinningTransformer(bins=bins)),
    ('woe', WOETransformer(columns=cols_to_keep)),
    ('xgb', XGBRegressor(n_estimators=100, random_state=seed))
])

# Clean and preprocess the data
# Handle missing values
data = df.dropna()

# Encode categorical variables
categorical_cols = ['term','home_ownership', 'verification_status']
data = pd.get_dummies(data, columns=categorical_cols)

# Scale the numerical variables
numerical_cols = ['loan_amnt', 'funded_amnt', 'funded_amnt_inv', 'int_rate', 'installment', 'annual_inc', 'total_acc', 'total_pymnt', 'total_pymnt_inv', 'total_rec_prncp', 'total_rec_int', 'last_pymnt_amnt']
data[numerical_cols] = (data[numerical_cols] - data[numerical_cols].mean()) / data[numerical_cols].std()

data = data.reset_index(drop=True)

# Definir X e Y
X = data.drop(['status'], axis=1)
Y = data['status']


# Dividir los datos en entrenamiento y prueba
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

## MODEL 3

model = XGBRegressor()
model.fit(X_train, Y_train)
# Realizar predicciones en los datos de prueba
Y_pred = model.predict(X_test)

# Evaluar la precisión del modelo
accuracy = accuracy_score(Y_test, Y_pred.round())
print("Precisión del modelo:", accuracy)

## Mandamos el modelod como PKL
with open("./Best_Model.pkl", "wb") as file:
    pickle.dump(model, file)




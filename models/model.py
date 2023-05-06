import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
from xgboost.sklearn import XGBRegressor
import sklearn.linear_model as slm
from sklearn.linear_model import BayesianRidge

## MODEL 1

#Raw Data
# Load the raw data into a Pandas DataFrame
data = pd.read_csv('credit_risk_data_v2.csv')

# Clean and preprocess the data
# Handle missing values
data = data.dropna()

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

model = LogisticRegression()

# Entrenar el modelo de regresión logística
model.fit(X_train, Y_train)

# Realizar predicciones en los datos de prueba
Y_pred = model.predict(X_test)

# Evaluar la precisión del modelo
accuracy = accuracy_score(Y_test, Y_pred)
print("Precisión del modelo:", accuracy)

## MODEL 2

model = BayesianRidge()
model.fit(X_train, Y_train)
# Realizar predicciones en los datos de prueba
Y_pred = model.predict(X_test)

# Evaluar la precisión del modelo
accuracy = accuracy_score(Y_test, Y_pred.round())
print("Precisión del modelo:", accuracy)


## MODEL 3

model = XGBRegressor()
model.fit(X_train, Y_train)
# Realizar predicciones en los datos de prueba
Y_pred = model.predict(X_test)

# Evaluar la precisión del modelo
accuracy = accuracy_score(Y_test, Y_pred.round())
print("Precisión del modelo:", accuracy)

with open("./model.pkl", "wb") as file:
    pickle.dump(model, file)
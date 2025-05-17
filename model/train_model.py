import pandas as pd
from prophet import Prophet
import pickle

df = pd.read_csv('data/TRM.csv')

df['ds'] = pd.to_datetime(df['ds'])
df['y'] = pd.to_numeric(df['y'], errors='coerce')

model = Prophet()
model.fit(df)

with open('model/trm_model.pkl', 'wb') as f:
  pickle.dump(model, f)

print("Modelo entrenado y guardado con éxito.")
import pandas as pd
import pickle
from prophet import Prophet
from datetime import datetime, timedelta

with open('model/trm_model.pkl', 'rb') as f:
  model = pickle.load(f)

def trm_prediction(start_date: str, end_date: str, usd_cost: float):
  try:
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')

    if start_date_dt > end_date_dt:
      return None, "Fecha inicial no puede ser mayor que la final."

    future = pd.date_range(start=start_date_dt, end=end_date_dt)
    df_future = pd.DataFrame({'ds': future})
    forecast = model.predict(df_future)
    forecast['costo_COP'] = forecast['yhat'] * usd_cost

    table = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'costo_COP']].rename(columns={
      'ds': 'Fecha',
      'yhat': 'TRM Predicha',
      'yhat_lower': 'TRM Mínima',
      'yhat_upper': 'TRM Máxima',
      'costo_COP': f'Costo Estimado en COP (${usd_cost} USD)'
    }).round(2).to_dict(orient='records')

    return table, None

  except Exception as e:
    return None, f"Error en los datos: {str(e)}"
import streamlit as st
import pandas as pd
import pickle
from prophet import Prophet
from datetime import datetime, timedelta

def check_password():
  pw = st.text_input("Contraseña", type="password")
  if pw == "trm2025":
    return True
  else:
    st.warning("Contraseña incorrecta.")
    return False

@st.cache_resource
def load_model():
  with open('model/trm_model.pkl', 'rb') as f:
    model = pickle.load(f)
  return model

def main():
  st.title("Predicción de la TRM y simulación de impacto en importaciones")

  if not check_password():
    return

  model = load_model()

  st.subheader("1. Selecciona un rango de fechas para predicción")
  start_date = st.date_input("Desde", value=datetime.today())
  end_date = st.date_input("Hasta", value=datetime.today() + timedelta(days=7))

  if start_date > end_date:
    st.error("La fecha inicial no puede ser posterior a la final.")
    return

  future = pd.date_range(start=start_date, end=end_date)
  df_future = pd.DataFrame({'ds': future})

  forecast = model.predict(df_future)

  st.subheader("Resultados de predicción TRM")
  st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(columns={
    'ds': 'Fecha',
    'yhat': 'TRM Predicha',
    'yhat_lower': 'TRM Mínima',
    'yhat_upper': 'TRM Máxima'
  }))

  st.line_chart(forecast.set_index('ds')[['yhat']], use_container_width=True)

  st.subheader("Simulación del impacto en costos de importación")
  costo_usd = st.number_input("Costo actual del producto en USD ($)", value=100.0)
  st.markdown("### Simulación del costo en pesos COP:")
  forecast['costo_COP'] = forecast['yhat'] * costo_usd
  st.dataframe(forecast[['ds', 'costo_COP']].rename(columns={
    'ds': 'Fecha',
    'costo_COP': f'Costo Estimado en COP (por ${costo_usd} USD)'
  }))

  st.line_chart(forecast.set_index('ds')[['costo_COP']], use_container_width=True)

if __name__ == "__main__":
  main()
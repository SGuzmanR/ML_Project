import pandas as pd

df = pd.read_csv('data/TRM_20250515.csv', encoding='utf-8', sep=',')
df['VIGENCIADESDE'] = pd.to_datetime(df['VIGENCIADESDE'], dayfirst=True)

df_clean = df[['VIGENCIADESDE', 'VALOR']].rename(columns={
  'VIGENCIADESDE': 'ds',
  'VALOR': 'y'
})
df_clean = df_clean.sort_values('ds')
df_clean.to_csv('data/TRM.csv', index=False)
print("Archivo limpio guardado como data/trm.csv")

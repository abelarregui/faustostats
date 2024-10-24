import streamlit as st
import pandas as pd

db = r'D:\Proyectos\Proyectos bet\2024\faustostats\faustostats\data\db\table_tennis_stats.csv'
# Título del dashboard
st.title("Fausto Stats - Table Tennis")

# Instrucción para subir el archivo
# archivo_csv = st.file_uploader("Sube tu archivo CSV", type=["csv"])


# Leer el CSV en un DataFrame
df = pd.read_csv(db)

# Mostrar el DataFrame
st.write("Vista previa de los datos:")
st.dataframe(df)

# Mostrar estadísticas básicas del DataFrame
st.write("Estadísticas descriptivas:")
st.write(df.describe())

# Mostrar las primeras filas del DataFrame
st.write("Primeras 5 filas:")
st.write(df.head())
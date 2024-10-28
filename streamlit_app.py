import streamlit as st
import pandas as pd
import plotly.express as px
from faustostats.utils.kpis import calculate_roi

db = r'https://raw.githubusercontent.com/abelarregui/faustostats/refs/heads/master/faustostats/data/db/table_tennis_stats.csv'
# db = r'D:\Proyectos\Proyectos bet\2024\faustostats\faustostats\data\db\table_tennis_stats.csv'
# Título del dashboard
st.title("Fausto Stats - Table Tennis")

# Instrucción para subir el archivo
# archivo_csv = st.file_uploader("Sube tu archivo CSV", type=["csv"])


# Leer el CSV en un DataFrame
df = pd.read_csv(db)
df = df.sort_values(by=['tournament_factor','time'])
# Mostrar el DataFrame
cols_show = ['time','tournament_factor','player_0','player_1','winner', 'profit', 'cumsum_profit','price_home','price_away','stake_home','stake_away','prob_home','prob_away',
             'cb_price_away','cb_price_home','cb_probability_away','cb_probability_home','sc_awayScore.current', 'sc_homeScore.current']


df_agg = calculate_roi(df)

# latest_cumsum = df.groupby('tournament_factor')['cumsum_profit'].last().reset_index()

# # Obtener el último valor de cumsum_profit por torneo
# latest_cumsum = df.groupby('tournament_factor')['cumsum_profit'].last().reset_index()
# latest_cumsum['cumsum_profit'] = latest_cumsum['cumsum_profit'].round(2)

# penultimate_cumsum = df.groupby('tournament_factor')['cumsum_profit'].apply(lambda x: x.iloc[-2] if len(x) > 1 else 0).reset_index()
# penultimate_cumsum.columns = ['tournament_factor', 'penultimate_profit']
# penultimate_cumsum['penultimate_profit'] = penultimate_cumsum['penultimate_profit'].round(2)


# Mostrar KPIs como métricas
st.header("Units won")
# Crear columnas

cols = st.columns(len(df_agg))

for i, col in enumerate(cols):
    print(i)
    col.metric(label=df_agg.reset_index().loc[i]['tournament_factor'], value=df_agg.reset_index().loc[i]['cumsum_profit'], 
            delta=df_agg.reset_index().loc[i]['roi'])


# Creamos una lista de columnas de Streamlit, con tantas columnas como filas tenga el DataFrame
# columns = st.columns(len(df))

# with columns[0]:
    
# Iteramos sobre cada fila y asignamos las métricas a cada columna
# for idx, row in df_agg.reset_index().iterrows():
#     with columns[idx]:
#         st.metric(label=row['tournament_factor'], value=f"Profit: {row['cumsum_profit']}", delta=f"ROI: {row['roi']}")


fig = px.line(
    df,
    x='time',
    y='cumsum_profit',
    color='tournament_factor',
    title='Profit Evolution',
    labels={'cumsum_profit': 'Cumsum Profit', 'time': 'Date'},
    template='plotly_white'
)

fig.update_layout(
    title_font=dict(size=24, color='#4A4A4A', family="Arial, sans-serif"),
    legend=dict(title='', font=dict(size=12)),
    xaxis_title='Date',
    yaxis_title='Cumsum Profit',
    xaxis=dict(showgrid=True, gridcolor='LightGrey'),
    yaxis=dict(showgrid=True, gridcolor='LightGrey')
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)


def highlight_row(row):
    if row['profit'] > 0:
        return ['background-color: lightgreen' for _ in row]  # Verde si > 0
    elif row['profit'] < 0:
        return ['background-color: lightcoral' for _ in row]  # Rojo claro si < 0
    else:
        return ['' for _ in row]

# Aplicar el estilo a todas las filas basado en los valores de 'Columna1'
styled_df = df[cols_show].style.apply(highlight_row, axis=1)


st.write("All the picks:")
st.dataframe(styled_df.format(precision=2), use_container_width=True)

# # Mostrar estadísticas básicas del DataFrame
# st.write("Estadísticas descriptivas:")
# st.write(df.describe())

# # Mostrar las primeras filas del DataFrame
# st.write("Primeras 5 filas:")
# st.write(df.head())
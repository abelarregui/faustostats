import streamlit as st
import pandas as pd
import plotly.express as px
from faustostats.utils.kpis import calculate_roi

db = r'https://raw.githubusercontent.com/abelarregui/faustostats/refs/heads/master/faustostats/data/db/table_tennis_stats.csv'
# db = r'D:\Proyectos\Proyectos bet\2024\faustostats\faustostats\data\db\table_tennis_stats.csv'

st.title("Fausto Stats - Table Tennis")

df = pd.read_csv(db)
df = df.sort_values(by=['tournament_factor','time'])

cols_show = ['time','tournament_factor','player_0','player_1','winner', 'profit', 'cumsum_profit','price_home','price_away','stake_home','stake_away','prob_home','prob_away',
             'cb_price_away','cb_price_home','cb_probability_away','cb_probability_home','sc_awayScore.current', 'sc_homeScore.current']

df_agg = calculate_roi(df)

st.header("Units won")
cols = st.columns(len(df_agg))

for i, col in enumerate(cols):
    col.metric(label=df_agg.reset_index().loc[i]['tournament_factor'], value=df_agg.reset_index().loc[i]['cumsum_profit'], 
            delta=df_agg.reset_index().loc[i]['roi'])

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

st.plotly_chart(fig)

def highlight_row(row):
    if row['profit'] > 0:
        return ['background-color: lightgreen' for _ in row]
    elif row['profit'] < 0:
        return ['background-color: lightcoral' for _ in row] 
    else:
        return ['' for _ in row]


styled_df = df[cols_show].style.apply(highlight_row, axis=1)

st.write("All the picks:")
st.dataframe(styled_df.format(precision=2), use_container_width=True)

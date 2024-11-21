import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
from faustostats.utils.kpis import calculate_roi, calculate_roi_by_weeks

db = r'https://raw.githubusercontent.com/abelarregui/faustostats/refs/heads/master/faustostats/data/db/table_tennis_stats.csv'
# db = r'D:\Proyectos\Proyectos bet\2024\faustostats\faustostats\data\db\table_tennis_stats.csv'

# Configuración de la página.

st.set_page_config(page_title="Fausto Stats", layout="wide")
# st.image(r"D:\Proyectos\Proyectos bet\2024\faustostats\logo.jpg", width=50)
st.subheader('FaustoStats')
df = pd.read_csv(db)
df = df.sort_values(by=['tournament_factor','time'], ascending=True)
df['time'] = pd.to_datetime(df['time'])
df['year-week'] = df['time'].dt.strftime('%Y-%U')
df_weeks = calculate_roi_by_weeks(df)

cols_show = ['time','tournament_factor','player_0','player_1','winner', 'profit', 'cumsum_profit','price_home','price_away','stake_home','stake_away','prob_home','prob_away',
             'cb_price_away','cb_price_home','cb_probability_away','cb_probability_home','sc_awayScore.current', 'sc_homeScore.current']

days_7_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
days_30_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
df_last_30 = df[df['time']>days_30_ago].copy()
df_last_7 = df[df['time']>days_7_ago].copy()
df_agg = calculate_roi(df)
df_agg_last30 = calculate_roi(df_last_30)
df_agg_last7 = calculate_roi(df_last_7)



tab_summary, tab_weeks, tab_max,  = st.tabs(['Summary',"By Weeks","Max"])

with tab_summary:
    # st.header("Units won")
    # df_agg_last7
    'Last 7 days'
    cols = st.columns(len(df_agg_last7))
    for i, col in enumerate(cols):
        col.metric(label=df_agg_last7.reset_index().loc[i]['tournament_factor'], value=df_agg_last7.reset_index().loc[i]['cumsum_profit'], 
                delta=df_agg_last7.reset_index().loc[i]['roi'])
    "---"
    'Last 30 days'
    cols = st.columns(len(df_agg_last30))
    for i, col in enumerate(cols):
        col.metric(label=df_agg_last30.reset_index().loc[i]['tournament_factor'], value=df_agg_last30.reset_index().loc[i]['cumsum_profit'], 
                delta=df_agg_last30.reset_index().loc[i]['roi'])
    "---"
    'All'
    cols = st.columns(len(df_agg))
    for i, col in enumerate(cols):
        col.metric(label=df_agg.reset_index().loc[i]['tournament_factor'], value=df_agg.reset_index().loc[i]['cumsum_profit'], 
                delta=df_agg.reset_index().loc[i]['roi'])
    "---"

with tab_weeks:
    fig = px.line(
        df_weeks,
        x='year-week',
        y='cumsum_profit_week',
        color='tournament_factor',
        title='Profit Evolution by Week',
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

    fig = px.line(
        df_weeks,
        x='year-week',
        y='roi',
        color='tournament_factor',
        title='ROI by Week',
        labels={'cumsum_profit': 'Cumsum Profit', 'time': 'Date'},
        template='plotly_white'
    )

    fig.update_layout(
        title_font=dict(size=24, color='#4A4A4A', family="Arial, sans-serif"),
        legend=dict(title='', font=dict(size=12)),
        xaxis_title='Date',
        yaxis_title='ROI',
        xaxis=dict(showgrid=True, gridcolor='LightGrey'),
        yaxis=dict(showgrid=True, gridcolor='LightGrey')
    )

    st.plotly_chart(fig)
    'Weeks'
    df_weeks

with tab_max:
    
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


    styled_df = df[cols_show].sort_values(by='time', ascending=False).style.apply(highlight_row, axis=1)

    st.write("All the picks:")
    st.dataframe(styled_df.format(precision=2), use_container_width=True, hide_index=True)

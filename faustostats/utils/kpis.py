
def calculate_roi(df):
    df['stake'] = df['stake_home'] + df['stake_away']
    df_agg = df.groupby('tournament_factor').agg({'stake':sum, 'cumsum_profit':'last'})
    df_agg['roi'] = (df_agg['cumsum_profit']/df_agg['stake'])*100
    df_agg = df_agg.round(2)
    return df_agg
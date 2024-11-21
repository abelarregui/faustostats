
def calculate_roi(df):
    df['stake'] = df['stake_home'] + df['stake_away']
    df['cumsum_profit'] = df.groupby('tournament_factor')['profit'].cumsum()
    df_agg = df.groupby('tournament_factor').agg({'stake':sum, 'cumsum_profit':'last'})
    df_agg['roi'] = (df_agg['cumsum_profit']/df_agg['stake'])*100
    df_agg = df_agg.round(2)
    return df_agg

def calculate_roi_by_weeks(df):
    df['stake'] = df['stake_home'] + df['stake_away']
    df['cumsum_profit_week'] = df.groupby(['tournament_factor','year-week'])['profit'].cumsum()
    df_agg_weeks = df.groupby(['tournament_factor','year-week']).agg({'stake':sum, 'cumsum_profit_week':'last'})
    df_agg_weeks['roi'] = (df_agg_weeks['cumsum_profit_week']/df_agg_weeks['stake'])*100
    df_agg_weeks = df_agg_weeks.round(2).reset_index()
    return df_agg_weeks
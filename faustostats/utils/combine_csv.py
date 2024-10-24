import pandas as pd
from pathlib import Path

def merge(path_input, path_output):
    # Directorio donde están los archivos CSV
    directorio = Path(path_input)

    # Paso 1: Obtener todos los archivos CSV en el directorio usando pathlib
    archivos_csv = list(directorio.glob('*.csv'))
    print('files:' , archivos_csv)

    # Paso 2: Leer y concatenar todos los CSV en un solo DataFrame
    dfs = []
    for archivo in archivos_csv:
        df = pd.read_csv(archivo) 
        df['tournament_factor'] = df['sc_tournament.slug'] + '_.' + archivo.stem.split('.')[-1]
        dfs.append(df)

    # dfs = [pd.read_csv(archivo) for archivo in archivos_csv]

    # Concatenar todos los DataFrames en uno solo
    df_final = pd.concat(dfs, ignore_index=True)
    df_final = calc_profit(df_final)

    df_final.to_csv(path_output+'/table_tennis_stats.csv')

def calc_profit(df):
    df.loc[df['winner']==0, 'profit'] = (df['price_home'] * df['stake_home']) - df['stake_home']
    df.loc[df['winner']==1, 'profit'] = (df['price_away'] * df['stake_away']) - df['stake_away']
    df.loc[df['profit']==0, 'profit'] = (df['stake_home'] + df['stake_away']) * -1
    df['cumsum_profit'] = df.groupby('tournament_factor')['profit'].cumsum()
    return df
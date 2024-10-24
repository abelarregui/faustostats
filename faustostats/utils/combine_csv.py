import pandas as pd
from pathlib import Path

def merge(path_input, path_output):
    # Directorio donde están los archivos CSV
    directorio = Path(path_input)

    # Paso 1: Obtener todos los archivos CSV en el directorio usando pathlib
    archivos_csv = list(directorio.glob('*.csv'))
    print('files:' , archivos_csv)

    # Paso 2: Leer y concatenar todos los CSV en un solo DataFrame
    dfs = [pd.read_csv(archivo) for archivo in archivos_csv]

    # Concatenar todos los DataFrames en uno solo
    df_final = pd.concat(dfs, ignore_index=True)
    df_final.to_csv(path_output+'/table_tennis_stats.csv')
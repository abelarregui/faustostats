import pandas as pd
import numpy as np
from numba import njit

def calc_payment_table(df_weeks):
    df_weeks_pivot = df_weeks.pivot_table(index="year-week", columns="tournament_factor", values=["cumsum_profit_week"])
    df_weeks_pivot_lite=df_weeks_pivot['cumsum_profit_week'][['Czech .9 apuestes','Elite .93 apuestes']]
    df_weeks_pivot_lite.fillna(0, inplace=True)
    df_weeks_pivot_lite['week_balance'] = df_weeks_pivot_lite['Czech .9 apuestes'] + df_weeks_pivot_lite['Elite .93 apuestes']
    new_col = calc_new_value(df_weeks_pivot_lite['week_balance'].values)
    df_weeks_pivot_lite['Accumulated'] = new_col

    df_weeks_pivot_lite['week_balance uds'] = df_weeks_pivot_lite['week_balance']/50
    df_weeks_pivot_lite['Accumulated uds'] = df_weeks_pivot_lite['Accumulated']/50
    df_weeks_pivot_lite['payment'] = df_weeks_pivot_lite['Accumulated uds'] * 20
    df_weeks_pivot_lite.loc[df_weeks_pivot_lite['payment']<0, 'payment'] = 0

    return df_weeks_pivot_lite

@njit
def calc_new_value(valores):
    n = len(valores)
    resultado = np.empty(n, dtype=np.float64)
    deuda = 0.0
    for i in range(n):
        # Si el valor es negativo, se registra y se suma la deuda
        if valores[i] < 0:
            resultado[i] = valores[i]
            deuda += -valores[i]  # sumamos la deuda en valor absoluto
        # Si hay deuda acumulada y el valor es positivo:
        elif deuda > 0:
            # Si el valor es suficiente para saldar la deuda:
            if valores[i] >= deuda:
                resultado[i] = valores[i] - deuda
                deuda = 0.0
            # Si el valor no alcanza para cubrir la deuda:
            else:
                resultado[i] = valores[i] - deuda  # resultado negativo
                deuda -= valores[i]
        # Si no hay deuda, se mantiene el valor original
        else:
            resultado[i] = valores[i]
    return resultado



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from chat_processing import generate_df

def characters_per_day(name, directorio):
    df = generate_df(name)

    df['Longitud'] = df['Mensaje'].apply(lambda x: len(x))

    caracteres_por_dia = df.groupby('Fecha')['Longitud'].sum()

    rango_fechas = pd.date_range(start=caracteres_por_dia.index.min(), end=caracteres_por_dia.index.max())

    caracteres_por_dia = caracteres_por_dia.reindex(rango_fechas, fill_value=0)

    media_movil_15d = caracteres_por_dia.rolling(window=15, center=True).mean()

    plt.figure(figsize=(20, 12))

    for i in range(1, len(caracteres_por_dia)):
        if caracteres_por_dia[i] == 0 and ( i-1>=0 and caracteres_por_dia[i-1] == 0):
            plt.plot(caracteres_por_dia.index[i-1:i+1], caracteres_por_dia.values[i-1:i+1], color='red')
        else:
            plt.plot(caracteres_por_dia.index[i-1:i+1], caracteres_por_dia.values[i-1:i+1], color='blue')

    plt.plot(caracteres_por_dia.index, media_movil_15d, color='magenta', label='Media móvil 15 días')

    plt.title('Número de carácteres por día')
    plt.xlabel('Fecha')
    plt.ylabel('Número de carácteres')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()

    nombre_archivo = os.path.join(directorio, 'characters_per_day.png')
    plt.savefig(nombre_archivo)
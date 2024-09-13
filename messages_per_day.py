import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from chat_processing import generate_df

def messages_per_day(name, directorio):

    df = generate_df(name)

    mensajes_por_dia = df.groupby('Fecha').size()

    rango_fechas = pd.date_range(start=mensajes_por_dia.index.min(), end=mensajes_por_dia.index.max())

    mensajes_por_dia = mensajes_por_dia.reindex(rango_fechas, fill_value=0)

    media_movil_15d = mensajes_por_dia.rolling(window=15, center=True).mean()

    plt.figure(figsize=(20, 12))

    for i in range(1, len(mensajes_por_dia)):
        if mensajes_por_dia[i] == 0 and ( i-1>=0 and mensajes_por_dia[i-1] == 0):
            plt.plot(mensajes_por_dia.index[i-1:i+1], mensajes_por_dia.values[i-1:i+1], color='red')
        else:
            plt.plot(mensajes_por_dia.index[i-1:i+1], mensajes_por_dia.values[i-1:i+1], color='blue')

    plt.plot(mensajes_por_dia.index, media_movil_15d, color='magenta', label='Media móvil 15 días')

    plt.title('Número de mensajes por día')
    plt.xlabel('Fecha')
    plt.ylabel('Número de mensajes')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()

    nombre_archivo = os.path.join(directorio, 'messages_per_day.png')
    plt.savefig(nombre_archivo)
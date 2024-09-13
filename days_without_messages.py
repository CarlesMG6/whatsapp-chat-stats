import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from chat_processing import generate_df

def days_without_messages(name, directorio):
    df = generate_df(name)

    mensajes_por_dia = df.groupby('Fecha').size()

    rango_fechas = pd.date_range(start=mensajes_por_dia.index.min(), end=mensajes_por_dia.index.max())

    mensajes_por_dia = mensajes_por_dia.reindex(rango_fechas, fill_value=0)

    dias_sin_mensajes = mensajes_por_dia.apply(lambda x: 0 if x != 0 else 1)

    suma = 0
    dias_desde_ultimo_mensaje = []
    for valor in dias_sin_mensajes:
        if valor == 0:
            suma = 0
            dias_desde_ultimo_mensaje.append(0)
        else:
            suma = suma + 1
            dias_desde_ultimo_mensaje.append(suma)

    serie_dias_desde_ultimo_mensaje = pd.Series(dias_desde_ultimo_mensaje)


    plt.figure(figsize=(10, 6))
    sns.lineplot(x=mensajes_por_dia.index, y=serie_dias_desde_ultimo_mensaje)

    plt.title('Días desde el último mensaje')
    plt.xlabel('Fecha')
    plt.ylabel('Días desde el último mensaje')
    plt.xticks(rotation=45)
    plt.grid(True)

    nombre_archivo = os.path.join(directorio, 'days_without_messages.png')
    plt.savefig(nombre_archivo)

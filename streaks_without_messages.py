import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from chat_processing import generate_df

def print_messages(df, type, message):

    print("\n\n ---------------- " + message + " -------------------- \n")

    messages_percentage = df.groupby([type])[type].count()
    print(messages_percentage)
    print("\n")

    gap_list = [1,5,10,25]
    for index in range(len(gap_list)):
        if(index<len(gap_list)-1):
            messages_interval = df[
                    (df['duracion'] >= gap_list[index] ) 
                    & ( df['duracion']< gap_list[index+1]) 
                ].groupby([type])['duracion'].count()
            print("Between " + str(gap_list[index]) + " and " + str(gap_list[index+1]) + " days")
        else:
            messages_interval = df[
                df['duracion'] >= gap_list[index] 
                ].groupby([type])['duracion'].count()
            print("Over " + str(gap_list[index])  + " days")
        print(messages_interval)
        print("\n")

def streaks_without_messages(name, directorio):
    df = generate_df(name)

    mensajes_por_dia = df.groupby('Fecha').size()

    rango_fechas = pd.date_range(start=mensajes_por_dia.index.min(), end=mensajes_por_dia.index.max())

    mensajes_por_dia = mensajes_por_dia.reindex(rango_fechas, fill_value=0)

    dias_sin_mensajes = mensajes_por_dia.apply(lambda x: 0 if x != 0 else 1)

    def recuperar_mensaje(day):
        for index, mensaje_en_dia in df[df['Fecha'] == day].iterrows():
                return mensaje_en_dia['Persona']

    def recuperar_last_mensaje(day):
        for index, mensaje_en_dia in df[df['Fecha'] == day].iterrows():
            mensaje = mensaje_en_dia['Persona']
        return mensaje


    suma = 0
    rachas_sin_mensajes = []
    dia_inicial = None
    for indice, valor in enumerate(dias_sin_mensajes):
        if valor == 0:
            if dia_inicial == None:
                suma = 0
                dia_inicial = mensajes_por_dia.index[indice]
            else: 
                if suma > 0:
                    mensajes_inicial = recuperar_last_mensaje(dia_inicial)
                    mensajes_final = recuperar_mensaje(mensajes_por_dia.index[indice])
                    racha = [dia_inicial, mensajes_por_dia.index[indice], suma, mensajes_inicial, mensajes_final]
                    rachas_sin_mensajes.append(racha)
                    suma = 0
                dia_inicial = mensajes_por_dia.index[indice]
        else:
            suma = suma + 1

    df_rachas_sin_mensajes = pd.DataFrame(rachas_sin_mensajes, columns=['incio', 'fin', 'duracion', 'mensajes_inicio', 'mensajes_final'])

    print_messages(df_rachas_sin_mensajes,'mensajes_inicio', 'Últimos mensajes al dejar de hablar')

    print_messages(df_rachas_sin_mensajes,'mensajes_final', 'Primeros mensajes al volver a hablar')



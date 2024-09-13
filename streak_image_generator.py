from PIL import Image, ImageDraw, ImageFont
import textwrap
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import math
from chat_processing import generate_df

def recuperar_mensajes(day, df):
    NUMBER_OF_MESSAGES = 6
    messages = []
    i = 0
    for index, mensaje_en_dia in df[df['Fecha'] == day].iterrows():
        if(i<NUMBER_OF_MESSAGES):
            i=i+1
            messages.append(mensaje_en_dia)
        else:
            break
    return messages 

def recuperar_last_mensajes(day, df):
    NUMBER_OF_MESSAGES = 6
    mensajes_del_dia = df[df['Fecha'] == day].copy()
    last_messages = mensajes_del_dia.tail(NUMBER_OF_MESSAGES)

    i = 0
    messages = []
    for index, mensaje_en_dia in last_messages.iterrows():
        if(i<NUMBER_OF_MESSAGES):
            i=i+1
            messages.append(mensaje_en_dia)
        else:
            break
    return messages

def generar_imagen_racha(racha, directorio):

    MAX_WIDTH = 100
    GAP_BT_PAR = 25
    GAP_BT_LINES = 15

    inicio, fin, duracion, mensajes_inicio, mensajes_final = racha

    inicio = inicio.date()
    fin = fin.date()
    
    img_width, img_height = 800, 600
    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 14)
        bigfont = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
        bigfont = ImageFont.load_default()

    # Título
    titulo = f"{duracion} días"
    draw.text((20, 20), titulo, fill="black", font=bigfont)
    
    # Fechas de inicio y fin
    fechas_texto = f"Inicio: {inicio}\n   Fin: {fin}"
    draw.text((400, 20), fechas_texto, fill="black", font=font)
    
    # Últimos mensajes antes de la racha
    y = 100
    draw.text((20, y), "Últimos mensajes:", fill="black", font=font)

    y+=GAP_BT_PAR

    for msg in mensajes_inicio:
        msg_text = f"{msg[0].date()} - {msg[1]}: {msg[2]} : {msg[3]}"
        wrapped_text = textwrap.fill(msg_text, width=MAX_WIDTH)
        draw.text((20, y), wrapped_text, fill="black", font=font)
        
        rows = math.floor(len(wrapped_text)/MAX_WIDTH)
        y += GAP_BT_PAR + GAP_BT_LINES*rows

    # Primeros mensajes después de la racha
    draw.text((20, y + 20), "Primeros mensajes:", fill="black", font=font)
    y += 40
    for msg in mensajes_final:
        msg_text = f"{msg[0].date()} - {msg[1]}: {msg[2]} : {msg[3]}"
        wrapped_text = textwrap.fill(msg_text, width=MAX_WIDTH)
        draw.text((20, y), wrapped_text, fill="black", font=font)

        rows = math.floor(len(wrapped_text)/MAX_WIDTH)
        y += GAP_BT_PAR + GAP_BT_LINES*rows

    path = f'{inicio}__{duracion}.png'

    nombre_archivo = os.path.join(directorio, path)
    img.save(nombre_archivo)

def streak_image_generator(name, directorio):

    directorio = directorio + '/streaks'

    if not os.path.exists(directorio):
        os.makedirs(directorio)

    df = generate_df(name)

    mensajes_por_dia = df.groupby('Fecha').size()

    rango_fechas = pd.date_range(start=mensajes_por_dia.index.min(), end=mensajes_por_dia.index.max())

    mensajes_por_dia = mensajes_por_dia.reindex(rango_fechas, fill_value=0)

    dias_sin_mensajes = mensajes_por_dia.apply(lambda x: 0 if x != 0 else 1)

    suma = 0
    rachas_sin_mensajes = []
    dia_inicial = None
    dia_final = None
    for indice, valor in enumerate(dias_sin_mensajes):
        if valor == 0:
            if dia_inicial == None:
                suma = 0
                dia_inicial = mensajes_por_dia.index[indice]
            else: 
                if suma > 0:
                    mensajes_inicial = recuperar_last_mensajes(dia_inicial, df)
                    mensajes_final = recuperar_mensajes(mensajes_por_dia.index[indice], df)
                    racha = [dia_inicial, mensajes_por_dia.index[indice], suma, mensajes_inicial, mensajes_final]
                    rachas_sin_mensajes.append(racha)
                    suma = 0
                dia_inicial = mensajes_por_dia.index[indice]
        else:
            suma = suma + 1

    df_rachas_sin_mensajes = pd.DataFrame(rachas_sin_mensajes, columns=['incio', 'fin', 'duracion', 'mensajes_inicio', 'mensajes_final'])

    for index, row in df_rachas_sin_mensajes.iterrows():
        generar_imagen_racha(row, directorio)


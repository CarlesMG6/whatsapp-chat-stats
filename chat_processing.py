import pandas as pd
import re

def generate_df(name):
    
    fechas = []
    horas = []
    personas = []
    mensajes = []
    patron_fecha = r'^\d{1,2}/\d{1,2}/\d{2}'

    with open('chats/'+name+'.txt', 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()
            
            if re.match(patron_fecha, linea[:8]):
                fecha_hora, resto = linea.split(' - ', 1)
                fecha, hora = fecha_hora.split(', ')
                persona, mensaje = resto.split(': ', 1)
                
                fechas.append(fecha)
                horas.append(hora)
                personas.append(persona)
                mensajes.append(mensaje)
            else:
                mensajes[-1] += ' ' + linea

    df = pd.DataFrame({
        'Fecha': fechas,
        'Hora': horas,
        'Persona': personas,
        'Mensaje': mensajes
    })

    df['Fecha'] = pd.to_datetime(df['Fecha'], dayfirst=True)

    return df
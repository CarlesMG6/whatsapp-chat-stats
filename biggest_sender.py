import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from chat_processing import generate_df

def biggest_sender(name, directorio):
    df = generate_df(name)

    df['Longitud'] = df['Mensaje'].apply(lambda x: len(x))

    # Number of messages
    sent_messages = df.groupby('Persona')['Persona'].count()
    plt.figure(figsize=(8, 6))
    sent_messages.plot(kind='pie', autopct='%1.1f%%', startangle=140)

    plt.title('Mensajes enviados')
    plt.ylabel('')

    nombre_archivo = os.path.join(directorio, 'sent_messages_by_person.png')
    plt.savefig(nombre_archivo)

    # Number of characters
    sent_characters = df.groupby('Persona')['Longitud'].sum()
    plt.figure(figsize=(8, 6))
    sent_characters.plot(kind='pie', autopct='%1.1f%%', startangle=140)

    plt.title('Carácteres enviados')
    plt.ylabel('')

    nombre_archivo = os.path.join(directorio, 'sent_characters_by_person.png')
    plt.savefig(nombre_archivo)



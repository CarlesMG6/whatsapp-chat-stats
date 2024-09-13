import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from chat_processing import generate_df

def mean_characters_per_message(name, directorio):
    df = generate_df(name)

    df['Longitud'] = df['Mensaje'].apply(lambda x: len(x))

    mean_characters_per_message = df.groupby('Persona')['Longitud'].mean()

    mean_characters_per_message = mean_characters_per_message.sort_values()

    colors = plt.cm.get_cmap('viridis', len(mean_characters_per_message))

    plt.figure(figsize=(10, 6))
    mean_characters_per_message.plot(kind='bar', color=[colors(i) for i in range(len(mean_characters_per_message))])

    plt.title('Media de Caracteres por Mensaje por Persona', fontsize=16)
    plt.xlabel('Personas', fontsize=14)
    plt.ylabel('Media de Caracteres por Mensaje', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    nombre_archivo = os.path.join(directorio, 'characters_per_message.png')
    plt.savefig(nombre_archivo)
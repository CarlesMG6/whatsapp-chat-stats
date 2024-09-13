import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from chat_processing import generate_df

def word_counter(name, directorio):

    directorio = directorio + '/word_counter'

    if not os.path.exists(directorio):
        os.makedirs(directorio)

    def clean_word(word):
        list_to_remove = [',','.','{','}','?','¿','[',']',')','(','"', ':', ';']
        for element in list_to_remove:
            word = word.replace(element,'')

        return word.lower()
    
    def not_valid_word(word):

        not_valid_words = ['', '<multimedia', 'omitido>', 'que', 'no', 'si', 'a', 'de', 'la', 'el', 'y', 'en', 'por', 'lo', 'es', 'me', 
                           'se', 'pero', 'por', 'un', 'las', 'ya', 'o', 'te', 'para', 'una', 'he', 'mi', 'los', 'al', 'como', 'del',
                           'ha']

        if word in not_valid_words:
            return True
        else:
            return False

    def insert_in_words_by_person(word, person, words):
        if word in words:
            people = words.get(word)
            if person in people:
                value = people.get(person) + 1
                people[person] = value
            else:
                people[person] = 1
        else: 
            people = {}
            people[person] = 1
            words[word] = people
        
    def insert_in_words(word, person, words):
        if word in words:
            value = words.get(word) + 1
            words[word] = value
        else:
            value = 1
            words[word] = value

    def generar_grafico(df_filtrado, persona_filtrada, titulo):
        plt.figure(figsize=(10, 6))
        plt.bar(df_filtrado['palabra'], df_filtrado['numero_de_veces'], color='skyblue')
        plt.title(f'Número de veces que {persona_filtrada} dijo cada palabra', fontsize=16)
        plt.xlabel('Palabras', fontsize=14)
        plt.ylabel('Número de veces', fontsize=14)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        titulo = clean_word(titulo)
        nombre_imagen = titulo + '.png'
        nombre_archivo = os.path.join(directorio, nombre_imagen)
        plt.savefig(nombre_archivo)

    df = generate_df(name)

    words_by_person = {}
    words_dict = {}
    for index, message_data in df.iterrows():
        message = message_data['Mensaje']
        person = message_data['Persona']
        words = message.split(' ')
        for word in words:
            word = clean_word(word)
            if not_valid_word(word):
                continue
            insert_in_words_by_person(word, person, words_by_person)
            insert_in_words(word, person, words_dict)

    data = []
    for word, people in words_by_person.items():
        for person, times in people.items():
            data.append((word, person, times))

    df = pd.DataFrame(data, columns=['palabra', 'persona', 'numero_de_veces'])

    df = df.sort_values('numero_de_veces', ascending=False)

    personas = df['persona'].unique()
    for persona_filtrada in personas:
        
        df_filtrado = df[df['persona'] == persona_filtrada].head(40)
        generar_grafico(df_filtrado, persona_filtrada, persona_filtrada)


    df_filtrado = df.groupby('palabra')['numero_de_veces'].sum().sort_values(ascending=False).head(40).reset_index()

    df_filtrado.columns = ['palabra', 'numero_de_veces']
    generar_grafico(df_filtrado, 'se', 'General')
        

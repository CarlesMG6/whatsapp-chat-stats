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
    
        not_valid_words = [
            '', '<multimedia', 'omitido>', 'null','no','si','mi','porque','perque',
            'a', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', 'durante', 'en', 'entre', 'hacia', 'hasta', ' mediante', 'para', 'por', 'según', 'sin', 'so', 'sobre', 'tras', 'versus', 
            'amb', 'cap', 'des', 'devers', 'envers', 'fins', 'malgrat', 'per', 'segons', 'sense', 'sobre', 'sota', 'ultra', 'vers',
            'así', 'asi', 'aunque', 'bien', 'como', 'conque', 'cuando', 'donde', 'e', 'entonces', 'esto', 'luego', 'mas', 'mientras', 'ni', 'o', 'pero', 'pese', 'pues', 'que', 'si', 'sino', 'u', 'y', 'ya',
            'ans', 'així', 'aixi', 'bé', 'be', 'com', 'doncs', 'e', 'encara', 'fins', 'i', 'ja', 'mentre', 'ni', 'o', 'però', 'pero', 'que', 'si', 'sinó', 'sino', 'u'
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
            'yo', 'tú', 'tu', 'él', 'el', 'ella', 'nosotros', 'vosotros', 'ellos', 'ellas', 'me', 'te', 'se', 'nos', 'os', 'lo', 'le', 'les', 'la', 'los', 'las',
            'que', 'quien', 'quién', 'cual', 'cuál', 'cuales', 'cuáles', 'este', 'ese', 'aquel', 'estos', 'esos', 'aquellos', 'esta', 'esa', 'aquella', 'estas', 'esas', 'aquellas',
            'el', 'la','al', 'els', 'les', 'un', 'una', 'uns', 'unes', 'del',
            'jo', 'tu', 'tú', 'ell', 'el', 'ella', 'nosaltres', 'vosaltres', 'ells', 'elles', 'em', 'et', 'es', 'ens', 'us', 'ho', 'li', 'els', 'la', 'les',
            'que', 'qui', 'què', 'que', 'cual', 'quin', 'quins', 'quina', 'quines', 'aquest', 'aquesta', 'aquests', 'aquestes', 'aquell', 'aquella', 'aquells', 'aquelles', 'això', 'aixo', 'allò', 'allo']
        
        extra_not_valid_words = [
            'muy', 'poco', 'bien', 'mal', 'aquí', 'alli', 'allí', 'ahora', 'hoy', 'ayer', 'siempre', 'nunca', 'ya', 'entonces', 'casi', 'pronto', 'lejos', 'cerca',
            'ah', 'eh', 'oh', 'pues', 'bueno', 'vaya',
            'molt', 'poc', 'bé', 'be', 'malament', 'aquí', 'aqui', 'allí', 'alli', 'ara', 'avui', 'ahir', 'sempre', 'mai', 'ja', 'aleshores', 'gairebé', 'aviat', 'lluny', 'aprop',
            'ah', 'eh', 'oh', 'doncs', 'bé', 'be', 'vaja',
            'soy', 'eres', 'es', 'somos', 'sois', 'son', 'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron', 'era', 'eras', 'éramos', 'éramos', 'eran', 'seré', 'serás', 'será', 'seremos', 'seréis', 'serán', 'eramos', 'seras', 'sera', 'seremos', 'sereis', 'seran',
            'estoy', 'estás', 'esta', 'está', 'estamos', 'estáis', 'estan', 'están', 'estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estaba', 'estabas', 'estábamos', 'estabais', 'estaban', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán','estas', 'esta', 'estais', 'estan', 'estuve', 'estuvimos', 'estuvieseis', 'estaban', 'estabas', 'estabamos', 'estare', 'estaras', 'estara', 'estaremos', 'estareis', 'estaran',
            'he', 'has', 'ha', 'hemos', 'habéis', 'han', 'había', 'habías', 'habíamos', 'habíais', 'habían', 'hube', 'hubiste', 'hubo', 'hubimos', 'hubisteis', 'hubieron', 'habré', 'habrás', 'habrá', 'habremos', 'habréis', 'habrán','habia', 'habias', 'habiamos', 'habiais', 'habian', 'habre', 'habras', 'habra', 'habremos', 'habreis', 'habran',
            'sóc', 'ets', 'és', 'som', 'sou', 'són', 'vaig', 'vas', 'va', 'vam', 'vau', 'van', 'era', 'eres', 'érem', 'éreu', 'eren', 'seré', 'seràs', 'serà', 'serem', 'sereu', 'seran',
            'estic', 'estàs', 'està', 'estem', 'esteu', 'estan', 'estava', 'estaves', 'estava', 'estàvem', 'estàveu', 'estaven', 'estaré', 'estaràs', 'estarà', 'estarem', 'estareu', 'estaran',
            'he', 'has', 'ha', 'hem', 'heu', 'han', 'havia', 'havies', 'havia', 'havíem', 'havíeu', 'havien', 'hauré', 'hauràs', 'haurà', 'haurem', 'haureu', 'hauran',
            'soc', 'ets', 'es', 'som', 'sou', 'son', 'erem', 'ereu', 'eren', 'seras', 'sera', 'serem', 'sereu', 'seran',
            'estas', 'esta', 'estem', 'esteu', 'estan', 'estava', 'estaves', 'estavem', 'estaveu', 'estaven', 'estare', 'estaras', 'estara', 'estarem', 'estareu', 'estaran',
            'havia', 'havies', 'haviem', 'havieu', 'havien', 'haure', 'hauras', 'haura', 'haurem', 'haureu', 'hauran'
            ]

        if word in not_valid_words:
            return True
        else:
            if word in extra_not_valid_words:
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
        

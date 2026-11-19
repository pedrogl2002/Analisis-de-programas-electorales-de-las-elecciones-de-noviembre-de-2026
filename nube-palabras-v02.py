from collections import Counter
import re
import matplotlib.pyplot as plt
from spacy.lang.es.stop_words import STOP_WORDS
from wordcloud import WordCloud

# 1. Define one key word per group with a list 
#of words/phrases to be considered as the same
groups = {
    'españa': ['español', 'españoles', 'española', 'españolas'] ,
    'trabajador' : ['trabajadora', 'trabajadores', 'trabajadoras'] ,
    'público' : ['pública', 'públicos', 'públicas'] ,
    'impuesto' : ['irpf', 'fiscal', 'fiscales', 'impuestos'] ,
    'mujer' : ['mujeres'] ,
    'hijo' : ['hija', 'hijos', 'hijas'] ,
    'europa' : ['europeo', 'europea', 'ue', 'europeos', 'europeas'] ,
    'economía' : ['económica', 'económico', 'económicas', 'económicos'] ,
    'familia' : ['familias'],
    'año' : ['años'] ,
    'ayuda' : ['ayudas'] ,
    'infraestructura' : ['infraestructuras'] ,
    'ley' : ['leyes'] ,
    'inversión' : ['inversiones'] ,
    'necesidad' : ['necesidades'] ,
    'libertad' : ['libertades'] ,
    'inversión' : ['inversiones'] ,
    'lucha' : ['luchar'] ,
    'recuperar' : ['recuperación'] ,
    'reducir' : ['reducción'] ,
    "empresa": ["empresas", "negocio", "negocios", "compañía", "compañías"],
}

# 2. Invert the dictionary: {variant: canonical_key}
word_to_group = {
    variant.lower(): key
    for key, variants in groups.items()
    for variant in variants
}
import os

# 3. Automatically find the folder where this script is saved
script_dir = os.path.dirname(os.path.abspath(__file__))

partido = 'Podemos'
file_path = os.path.join(script_dir, f"programa-{partido}.txt")

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read().lower()

# 4. Tokenize (matching multi-word variants first, then individual words)
multi_word_variants = sorted(
    [w for w in word_to_group if " " in w], key=len, reverse=True
)
if multi_word_variants:
    token_pattern = re.compile(
        r"\b(?:"
        + "|".join(re.escape(w) for w in multi_word_variants)
        + r"|\w+)\b"
    )
else:
    token_pattern = re.compile(r"\b\w+\b")

tokens = token_pattern.findall(text)

# 5. Filter stopwords and replace variants with their canonical group key
spanish_stopwords = set(STOP_WORDS)
spanish_stopwords.update(["ejemplo", "palabra", "además", "especialmente", "800", "díaz", "octubre", "mayo", "sánchez", "15", "enero", "sumar", "diciembre", "octubre", "junio", "psoe", "pedro", "29", "25", "60", "14", "2023", "2024", "2025", "2026", "2027", "2030", "julio", "000", "30", "10", "20", "programa", "irene", "partido", "montero", "abril", "noviembre"])

grouped_tokens = [
    word_to_group.get(token, token)
    for token in tokens
    if token not in spanish_stopwords and len(token) > 1
]

# 6. Count totals and generate the word cloud
word_counts = Counter(grouped_tokens)

wc = WordCloud(
    width=800,
    height=400,
    background_color="white",
    max_words = 75, 
).generate_from_frequencies(word_counts)

plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation="bilinear")
plt.title("Nube de palabras: Programa " + partido)
plt.axis("off")
plt.show()
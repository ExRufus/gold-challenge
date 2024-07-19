from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
import pandas as pd
import nltk
import re


# Download daftar stopwords bahasa Indonesia dari NLTK
nltk.download('stopwords')
stop_words = set(stopwords.words('indonesian'))

# Membuat objek StemmerFactory dan stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Fungsi untuk memuat alaymap dari CSV
def load_alaymap(csv_file):
    df = pd.read_csv(csv_file)
    alaymap = dict(zip(df['alias'], df['standard']))
    return alaymap

# Memuat alaymap dari file CSV
alaymap = load_alaymap('../archive/new_kamusalay.csv')

def lowercase(text):
    return text.lower()

def remove_unnecessary_char(text):
    text = re.sub(r'\n', ' ', text)  # Remove '\n' atau paragraf baru
    text = re.sub(r'rt', ' ', text)  # Remove retweet symbol
    text = re.sub(r'USER', ' ', text)  # Remove username
    text = re.sub(r'(https?://\S+)', ' ', text)  # Remove URL
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    return text

def remove_emoticon(text):
    ascii_emoticon_pattern = r'[:;=8][\-o\*\']?[\)\]\(\[dDpP/\:\}\{@\|\\]'
    unicode_emoticon_pattern = r'[\U0001F600-\U0001F64F\U263A-\U2764\U270B-\U1F910]'
    combined_pattern = f'({ascii_emoticon_pattern}|{unicode_emoticon_pattern})'
    text = re.sub(combined_pattern, '', text)
    return text

def remove_extra_spaces(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def remove_unicode(text):
    text = re.sub(r'\b[^\x00-\x7F]+\b', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def remove_nonalphabetic(text):
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    return text

def normalize_alay(text, alaymap):
    return ' '.join([alaymap[word] if word in alaymap else word for word in text.split(' ')])

def remove_stopwords(text, stopword_list):
    return ' '.join([word for word in text.split() if word not in stopword_list])

def stemming(text):
    return stemmer.stem(text)

def clean_text(text, alaymap, stopword_list):
    text = lowercase(text)
    text = remove_unnecessary_char(text)
    text = remove_emoticon(text)
    text = remove_extra_spaces(text)
    text = remove_unicode(text)
    text = remove_nonalphabetic(text)
    text = normalize_alay(text, alaymap)
    text = remove_stopwords(text, stopword_list)
    text = stemming(text)
    return text

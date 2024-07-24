import re
import unicodedata
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory # type: ignore

factory = StemmerFactory()
stemmer = factory.create_stemmer()

# membuat semua huruf menjadi kecil
def lowercase(text):
    return text.lower()

# menghilangkan character yang tidak perlu
def remove_unnecessary_char(text):
    text = re.sub(r'(@[\w]*|rt|https?://\S+|#\S+|\n)', ' ', text)
    text = re.sub(r'  +', ' ', text)
    return text.strip()

# menghilangkan emoticon
def remove_emoticon(text):
    ascii_emoticon_pattern = r'[:;=8][\-~]?[)\(DPOp]'
    unicode_emoticon_pattern = r'[\U0001F600-\U0001F64F]|\u263A-\u263C|\u2764|\u270B|\U0001F910-\U0001F92F|\U0001F300-\u0001F5FF|\U0001F680-\U0001F6FF|\U0001F700-\U0001F77F]'
    combined_pattern = f'{ascii_emoticon_pattern}|{unicode_emoticon_pattern}'
    text = re.sub(combined_pattern, '', text)
    return text

# hapus kata yang berawalan x-- yang diakhiri 2 heksadesimal
def remove_unicode(text):
    text = re.sub(r'\bx[a-fA-F0-9]{2}\b', '', text)
    text = re.sub(r'\bx([a-fA-F0-9]{2})', '', text)
    return text

def remove_nonaplhanumeric(text):
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
    return text

def normalize_alay(text, alaymap):
    return ' '.join([alaymap[word] if word in alaymap else word for word in text.split(' ')])

def remove_stopword(text, stopwords):
    text = ' '.join(['' if word in stopwords else word for word in text.split(' ')])
    text = re.sub('  +', ' ', text)
    text = text.strip()
    return text

def stemming(text, stemmer):
    return stemmer.stem(text)

def textpreprocess(text, stopwords, alaymap, stemmer):
    text = lowercase(text)
    text = remove_unnecessary_char(text)
    text = remove_emoticon(text)
    text = remove_unicode(text)
    text = remove_nonaplhanumeric(text)
    text = normalize_alay(text, alaymap)
    text = stemming(text, stemmer)
    text = remove_stopword(text, stopwords)
    return text

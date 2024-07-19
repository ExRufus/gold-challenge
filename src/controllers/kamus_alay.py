import pandas as pd
from utils.text_preprocessing import clean_text

# Membaca kamus alay dari file CSV
def read_alay_dictionary(file_path):
    df = pd.read_csv(file_path, encoding='latin1')
    alay_map = pd.Series(df.iloc[:, 1].values, index=df.iloc[:, 0]).to_dict()
    return alay_map

# File paths 
alay_dict_file = 'kamus_alay.csv'
# stopwords_file = 'stopwords.txt'
input_text_file = 'input.txt'
output_text_file = 'output.txt'

# Membaca kamus alay dan stopwords
# alay_dict = read_alay_dictionary(alay_dict_file)
# stopwords = read_stopwords(stopwords_file)

# Fungsi untuk membaca stopword list dari file teks
def read_stopwords(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        stopwords = file.read().splitlines()
    return stopwords

# Memproses teks dari file input
def process_text(input_file, output_file, alay_dict, stopwords):
    with open(input_file, mode='r', encoding='utf-8') as file:
        text = file.read()
    
    cleaned_text = clean_text(text, alay_dict, stopwords)
    
    with open(output_file, mode='w', encoding='utf-8') as file:
        file.write(cleaned_text)

# Menjalankan proses pembersihan teks
process_text(input_text_file, output_text_file, alay_dict) # , stopwords

print("Teks telah diproses dan disimpan ke", output_text_file)

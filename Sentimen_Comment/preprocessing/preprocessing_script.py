import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

# Download dulu stopwords (1x aja)
nltk.download('stopwords')

stop_words = set(stopwords.words('indonesian'))  # bisa ganti 'english' kalau pakai English
stemmer = PorterStemmer()

def preprocess_text_advanced(text):
    # 1. Lowercase
    text = text.lower()

    # 2. Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # 3. Tokenization
    tokens = text.split()

    # 4. Remove stopwords
    tokens = [word for word in tokens if word not in stop_words]

    # 5. Stemming (pakai stemming English aja biar simpel, kalau Indo bisa pakai Sastrawi stemmer)
    tokens = [stemmer.stem(word) for word in tokens]

    return tokens

preprocessed_tokens_adv = preprocess_text_advanced(text)
print(preprocessed_tokens_adv)

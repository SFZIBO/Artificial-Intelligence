from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    input_text = None
    if request.method == 'POST':
        input_text = request.form['user_input']
        # Dummy prediksi → nanti diganti prediksi asli
        result = 'Positif' if 'bagus' in input_text else 'Negatif'
    return render_template('index.html', result=result, input_text=input_text)

@app.route('/predict', methods=['POST'])
def predict():
    user_input = request.form.get('user_input')
    
    if not user_input.strip():
        return "Komentar kosong. Silakan masukkan teks.", 400

    sentiment = get_sentiment(user_input)

    return render_template('index.html', sentiment=sentiment)


def get_sentiment(text):
    keywords_positif = [
        'bagus', 'mantap', 'keren', 'oke', 'hebat', 'top', 'lancar',
        'amazing', 'luar biasa', 'suka', 'love', 'terbaik', 'menarik',
        'recommended', 'rekomendasi', 'happy', 'puas', 'senang', 'perfect',
        'ciamik', 'kece', 'juara', 'worth it', 'berhasil', 'mulus',
        'gemilang', 'bagus banget', 'bagus sekali', 'gg', 'good game',
        'sip', 'mantep', 'keren banget', 'solid', 'trusted', 'fast respon',
        'bagus lah', 'works', 'okelah', 'supportive', 'cool', 'bestie',
        'helpful', 'memuaskan', 'efisien', 'praktis', 'asik', 'asikk',
        'the best', 'stabil', 'smooth', 'cepat', 'responsif', 'smart',
        'brilian', 'inovatif', 'kualitas oke'
    ]
    keywords_negatif = [
        'jelek', 'buruk', 'parah', 'gagal', 'lemot', 'lambat', 'nge-lag',
        'error', 'crash', 'down', 'bohong', 'rip-off', 'jelek banget',
        'sampah', 'ngecewain', 'nggak puas', 'jelek sekali', 'mengecewakan',
        'toxic', 'tidak rekomendasi', 'ripuh', 'zonk', 'ga worth it',
        'aneh', 'aneh banget', 'laggy', 'broken', 'uninstall', 'kapok',
        'nipu', 'scam', 'fraud', 'palsu', 'fake', 'gimmick', 'trik busuk',
        'tidak sesuai', 'cacat', 'bug', 'bugs', 'malware', 'lemot banget',
        'hang', 'kerusakan', 'kacau', 'tidak stabil', 'tidak lancar',
        'curang', 'kurang ajar', 'malesin', 'payah', 'lelet', 'bikin kesel',
        'ngeframe', 'noob', 'ga jelas', 'ga mutu', 'gagal paham', 'ngaco',
        'nggak jelas', 'nggak ada gunanya', 'nggak bermanfaat', 'nggak enak', 'fufufafa',
        'nggak worth it', 'nggak recommended', 'nggak suka', 'nggak nyaman',
        'masalah', 'problem', 'rusak', 'ngegas', 'ribet', 'nyebelin'
    ]


    text_lower = text.lower()
    if any(word in text_lower for word in keywords_positif):
        return 'positif'
    elif any(word in text_lower for word in keywords_negatif):
        return 'negatif'
    else:
        return 'netral'
    
if __name__ == '__main__':
    app.run(debug=True)

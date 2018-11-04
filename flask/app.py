# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for
import json
import google_ocr
from functions import *

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    # index.html をレンダリングする
    return render_template('index.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/edit', methods=['POST', 'GET'])
def edit():
    # imageファイルを保存する
    img_file = request.files['upfile']
    img_file.save("./camera_data/sample.jpg")

    # ファイルをOCRにかける
    api_key = "AIzaSyDNDH54qwYoqAs_qXSyYsBjWUfcXbdk6uA"
    image_filenames = ["./camera_data/sample.jpg"]
    response = google_ocr.request_ocr(api_key, image_filenames)
    if response.status_code != 200 or response.json().get('error'):
        # print(response.text)
        return render_template('edit.html', letter_body="")
    else:
        with open('./camera_data/sample.jpg.json', 'w', encoding='utf-8') as fp:
            fp.write(json.dumps(response.json(), ensure_ascii=False))

        try:
            letter_body = response.json()["responses"][0]["textAnnotations"][0]["description"]
        except:
            letter_body = ""
        return render_template('edit.html', letter_body=letter_body)


@app.route('/result', methods=['POST'])
def result():
    letter_body = request.form["letter_body"]
    print("取得文字列")
    print(letter_body)
    # らいきの関数を呼ぶ

    vectors_list = letter_to_vector(letter_body)
    results_list = get_similar_flowers_list(vectors_list)
    #もらったデータと花データベースを比較し、似ている数個をピックアップ
    # print(results_list)

    return render_template('result.html', results=results_list)

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に

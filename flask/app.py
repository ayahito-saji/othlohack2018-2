# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for

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

@app.route('/edit', methods=['POST'])
def edit():
    return render_template('edit.html')

@app.route('/result', methods=['POST'])
def result():
    # らいきの関数を呼ぶ

    #もらったデータと花データベースを比較し、似ている数個をピックアップ


    return render_template('result.html')

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に

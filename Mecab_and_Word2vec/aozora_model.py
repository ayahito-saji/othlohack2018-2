# Word2Vecライブラリのロード
from gensim.models import word2vec
import os
import re
import MeCab

path_ds = list(os.walk('./aozora'))
path_list = path_ds[0][2]


# ファイル読込み、内部表現化
wakati_list = []
for path in path_list:
    path = "./aozora/"+path
    try:
        f = open(path, "r")
        text = f.read()
        f.close()
    except Exception as e:
        print(e)
        print(path)
        continue

    # ヘッダ部分の除去
    try:
        text = re.split('\-{5,}',text)[2]
    except Exception as e:
        continue

    # フッタ部分の除去
    text = re.split('底本：',text)[0]
    # | の除去
    text = text.replace('|', '')
    # ルビの削除
    text = re.sub('《.+?》', '', text)
    # 入力注の削除
    text = re.sub('［＃.+?］', '',text)
    # 空行の削除
    text = re.sub('\n\n', '\n', text)
    text = re.sub('\r', '', text)
    text = text.replace('\u3000', '')

    #一行ごとに仲間分け
    lines = [re.sub('\n', "", t) for t in text.split("。")]

    M = MeCab.Tagger("-Ochasen")

    for line in lines:
        ms = M.parse(line).split("\n")
        line_list = []
        for m in ms:
            m = m.split()
            if len(m) < 4:
                continue
            if not "名詞" in m[3] and not "動詞" in m[3]:
                continue
            line_list += [m[0]]
        # line_str = " ".join(line_list)
        # wakati_list += [line_str]
        wakati_list += [line_list]

# f = open("wakati_text.txt", 'w', encoding='utf-8_sig')
# f.write('\n'.join(wakati_list))
# f.close()
# print(wakati_list)

# model = word2vec.Word2Vec('wakati_text.txt', size=100, min_count=3,window=5,iter=100)
model = word2vec.Word2Vec(wakati_list, size=100, min_count=3,window=5,iter=100)
ret = model.wv.most_similar(positive=['愛'])
model.wv.save_word2vec_format("./text",binary=True)

#単語ベクトル化
# print(model["愛"])
for item in ret:
    print(item[0], item[1])
print("ok")

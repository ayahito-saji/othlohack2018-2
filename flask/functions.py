import json
import sys
import MeCab
from gensim.models import KeyedVectors
import numpy as np
import re
from threading import Lock

class Model(object):

    _model = None
    _model_instance = None
    _lock = Lock()

    def __new__(cls):
        raise NotImplementedError("nanndemoiiyomozi")

    @classmethod
    def __internal_new__(cls):
        return super().__new__(cls)

    @classmethod
    def get_instance(cls):
        if not cls._model_instance:
            with cls._lock:
                if not cls._model_instance:
                    cls._model_instance = cls.__internal_new__()
                    file_name = "./jawiki_studied_data.bin"
                    cls._model = KeyedVectors.load_word2vec_format(file_name, binary=True)
        return cls._model_instance

    @staticmethod
    def keep():
        print("aa")




def letter_to_vector(letter):
    model = Model.get_instance()._model

    M = MeCab.Tagger()

    dear = re.findall("([a-zA-Zぁ-んァ-ン一-龥]+)(ちゃん|くん|さん|さま|君|様)?へ", letter)
    if len(dear) != 0:
        dear = re.sub("(ちゃん|くん|さん|さま|君|様)", "", dear[0][0])
        letter = letter.replace(dear, "")

    # print(dear)
    from_ = re.findall("([a-zA-Zぁ-んァ-ン一-龥]+)(より)$", letter)

    if len(from_) != 0:
        from_ = from_[0][0]
        letter = letter.replace(from_, "").replace("より", "")

    letter = re.sub("[\n。　]", " ", letter)

    print(letter)

    letter_and_vector_list = {}
    vecs_list = []
    results = M.parse(letter)

    for result_line in results.split("\n"):
        dump_list = []
        result = result_line.split()
        if len(result) == 2:
            surface = result[0]
            features = result[1].split(',')
            if features[0] in ["動詞", "形容詞"]:
                dump_list += [features[6]]
            elif features[0] in ["名詞", "連体詞", "副詞"]:
                dump_list += [surface]
        else:
            continue
        if (len(dump_list) == 0):
            continue

        print(dump_list)
        flag = -1
        while (flag < 0 and len(dump_list)):
            try:
                vecs_list = np.array(model[dump_list])
                flag = 1
            except Exception as e:
                temp_list = []
                for dum in dump_list:
                    print(str(e))
                    if dum in str(e):
                        continue
                    temp_list += [dum]
                dump_list = temp_list
                flag -= 1
        if len(dump_list) == 0:
            continue

        vec = np.mean(vecs_list, axis=0)

        letter_and_vector_list[dump_list[0]] = vec

    return letter_and_vector_list


def get_similar_flowers_list(vectors_list):
    results = []
    count = {}

    # ベクトル量の合計を記録する辞書型を設定
    letter = open('./flower_to_vec.json', 'r', encoding="utf-8_sig")
    flowers = json.load(letter)
    letter.close()

    # 手紙の文字と花言葉のベクトル量のユークリッド距離を求めて記録
    def search(a, count=count, flowers=flowers):
        for flower in flowers:
            dict = {}
            for key, vec in flower['vec_dict'].items():
                dif = np.linalg.norm(np.array(a) - np.array(vec))
                count[flower['name']][key] += dif
        return count


    for flower in flowers:
        count[flower['name']] = {}
        for key, vec in flower['vec_dict'].items():
            count[flower['name']][key] = 0

    # 検索
    for key,value in vectors_list.items():
        count = search(value)

    # リストに要素を追加
    for key, vec in count.items():
        for word, dif in vec.items():
            for flower in flowers:
                if (flower["name"] != key):
                    continue
                flower_words = list(flower["vec_dict"].keys())
                break
            results.append([dif, key, word, flower_words])

    # リストをソート
    results = sorted(results, key=lambda x: x[0])
    # ranking_list = [[x[1],x[2]]for x in results[0:15]]
    return_list = [[x[1], x[2], x[3]] for x in results]
    return return_list[0:20]
    # print(ranking_list)

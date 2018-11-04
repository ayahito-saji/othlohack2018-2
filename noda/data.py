import json
import numpy as np
results = []
count = {}

#ベクトル量の合計を記録する辞書型を設定
letter = open('flower_to_vec.json' , 'r',encoding="utf-8_sig")
flowers = json.load(letter)
for flower in flowers:
    count[flower['name']] = {}
    for key,vec in flower['vec_dict'].items():
        count[flower['name']][key] = 0

#手紙の文字と花言葉のベクトル量のユークリッド距離を求めて記録
def search(a,count = count,flowers = flowers):
    for flower in flowers:
        dict ={}
        for key,vec in flower['vec_dict'].items():
            dif = np.linalg.norm(np.array(a)-np.array(vec))
            count[flower['name']][key] += dif
    return count
    
#来期データ

#検索
for key,value in a.items():
    count = search(value)

#リストに要素を追加
for key,vec in count.items():
    for word,dif in vec.items():
        for flower in flowers:
            if (flower["name"] != key):
                continue
            flower_words = list(flower["vec_dict"].keys())
            break
        results.append([dif,key,word,flower_words])

#リストをソート
results = sorted(results, key=lambda x:x[0])
#ranking_list = [[x[1],x[2]]for x in results[0:15]]
return_list = [[x[1], x[2],x[3]] for x in results]
print(return_list[0:20])
#print(ranking_list)

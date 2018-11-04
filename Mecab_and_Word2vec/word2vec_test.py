from gensim.models import word2vec

model = word2vec.Word2Vec(wakati_list, size=100, min_count=3,window=5,iter=100)
ret = model.wv.most_similar(positive=['愛する人'])
model.wv.save_word2vec_format("./text",binary=True)

for item in ret:
    print(item[0], item[1])
print("ok")

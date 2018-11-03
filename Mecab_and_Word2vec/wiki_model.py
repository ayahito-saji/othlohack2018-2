from gensim.models import KeyedVectors
file_name = "./txt/entity_vector.model.bin"

model = KeyedVectors.load_word2vec_format(file_name, binary=True)
# model = word2vec.Word2Vec("", size=100, min_count=3,window=5,iter=100)
# model.wv.save_word2vec_format("./text",binary=True)
ret = model.wv.most_similar(positive=[''])

for item in ret:
    print(item[0], item[1])

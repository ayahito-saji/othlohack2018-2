import sys
import MeCab
M = MeCab.Tagger("-Ochasen")
# m = MeCab.Tagger("-Owakati")
ms = M.parse("愛する人よ、永遠に眠れ")
wakachi_list = []
for m in ms:
    m = m.split()
    if len(m) < 4:
        continue
    if not "名詞" in m[3] and not "動詞" in m[3]:
        continue
    wakachi_list += [m[0]]
print(wakachi_list)
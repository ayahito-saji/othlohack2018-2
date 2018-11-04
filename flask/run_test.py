import json
import sys
import MeCab
from gensim.models import KeyedVectors
import numpy as np
import re
from functions import *

letter_body = """

初めまして世界

ようこそ世界

またね

"""
vectors_list = letter_to_vector(letter_body)
results_list = get_similar_flowers_list(vectors_list)
# もらったデータと花データベースを比較し、似ている数個をピックアップ
print(results_list)

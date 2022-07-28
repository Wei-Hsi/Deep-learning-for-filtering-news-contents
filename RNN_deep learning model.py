# -*- coding: utf-8 -*-
"""Deep learning for filtering news contents

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VUwpB9_Ydr3MDrEszOOQpPKMZcCPgPoi

### Introduction

Nowadays, unsuitable news content for under 12-year-old children is increasing in Taiwan. Those violent, bloody, and pornographic content should be restricted. To protect these young audiences' mental health, I build a deep learning model that can avoid them from reaching these types of news. In the project, I build the RNN(Recurrent Neural Network) model with Python, and every detailed step is below.
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import numpy as np
import pandas as pd
import matplotlib.pyplot
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding
from tensorflow.keras.layers import LSTM

"""### 01. Import text data 

1.   First, using Python to crawl news websites and grab the news headlines.
2.   Artificially mark all news headlines as "0" and "1". (0 refers to the warning; 1 refers to allow to read)
3.   Save as a CSV file and upload to google drive.
"""

from google.colab import drive

drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd '/content/drive/My Drive/Colab Notebooks'

df = pd.read_csv('NewsTitle2.csv',sep=",")

df.head()

"""### 02. Keep text only in Chinese

Numbers in news headlines do not affect deep learning too much. Use the regular expression (`re`) to remove all the numbers.

"""

import re

"""The range for Chinese characters in the Unicode is "u4E00 - u9FD5"."""

patn=re.compile(r"[\u4E00-\u9FD5]+")

"""At the same time, separate the words in all sentences."""

for review in df['新聞標題']:
    print(patn.findall(review))

"""After removing numbers, use blank space to connect the words in all sentences."""

x_tmp = []

for review in df['新聞標題']:
    sen_list = patn.findall(review)
    sen = ' '.join(sen_list)
    x_tmp.append(sen)

x_tmp

"""### 03. Compute each word's frequency

Put all sentences in a string and count the number of occurrences for each word.
"""

egg = ''.join(''.join(x_tmp).split())

egg

count = {}

for char in egg:
    if char in count.keys():
        count[char] += 1
    else:
        count[char] = 1

count

"""### 04. Give each word a number

Sort the values ​​in the previous part, and give each word a number. (words that appear more often rank higher.)


"""

sorted(count, key=count.get,  reverse=True)

"""Use the `enumerate` function to give each word number from 1 to 3463 in order."""

egg = sorted(count, key=count.get,  reverse=True)

for i, char in enumerate(egg, 1):
    print(char, i)

"""Define the sorting result, and set it as a dictionary."""

sorted_char = {char: i for i, char in enumerate(egg, 1)}

"""Set the blank space as 0."""

sorted_char[" "] = 0

"""### 05. Encode all sentences

1.   Define a fuction that could make each word turn out to a code.(`char --> sorted_char[char]`)
2.   Use the `map` function to apply on all sentences.

"""

x = []

for review in x_tmp:
    record = list(map(lambda char:sorted_char[char], review))
    x.append(record)

y = df["是否適宜觀看"].values

y

"""### 06. Divide data into "train data" and "test data".

After testing, the ratio of 8:2 is the best training result.
"""

x_train = x[0:8000]

y_train = y[0:8000]

x_test = x[8000:10164]

y_test = y[8000:10164]

x_train = sequence.pad_sequences(x_train, maxlen=30)
x_test = sequence.pad_sequences(x_test, maxlen=30)

"""### 07. Build a deep learning model"""

model = Sequential()

model.add(Embedding(10000, 256))

model.add(LSTM(300, dropout=0.2, recurrent_dropout=0.2))

model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
             optimizer='adam',
             metrics=['accuracy'])

model.summary()

"""In the raw data, the ratio of "0" and "1" is 1:9. In order to get a better training result, balance the ratio of "0" and "1" by elevating the weight of "0"."""

from sklearn.utils import class_weight
print(np.unique(y_train))
weights = class_weight.compute_class_weight("balanced",np.unique(y_train),y_train)
weights = {i:weights[i] for i in range(2)}
print(weights)

"""### 08. Train the RNN model"""

model.fit(x_train, y_train, batch_size=32, epochs=5,
         validation_data=(x_test, y_test))

"""### 09. Test and Application"""

def predict(input):
  encode_input = list(map(lambda char:sorted_char[char],' '.join(patn.findall(input))))
  output = model.predict([encode_input])[0][0]
  print('Predicted probability: {}'.format(output))
  print('Prediction: {}'.format('banned' if output < 0.5 else 'passed'))

predict('少女爛醉認錯男友！嘿咻2次還想要　他躲室友房、她裸身拍門狂求歡酒醒嚇瘋')

predict('【獨家／醫師染疫1】首例確診醫師遭爆在院內未戴口罩　護理師女友同住中招')

predict('13歲女5月4度激戰3男　鷹眼媽靠房內一瓶礦泉水揪出真相')

predict('台中夜店流出「全裸女」3P片！開幕主打高爾宣　鹹濕試營運遭警嚴辦')
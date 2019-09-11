#!/usr/bin/env python
# coding: utf-8

# # Import Libraries

# In[1]:


from __future__ import absolute_import, division, print_function, unicode_literals

import os
import time
from datetime import datetime
from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from matplotlib.font_manager import FontProperties
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.optimizers import RMSprop
from tensorflow.python.keras.preprocessing import sequence
from tensorflow.python.keras.preprocessing.text import Tokenizer

from common import logger_factory
from common import path_config

## fonts = FontProperties(fname = "/Library/Fonts/华文细黑.ttf",size=14)
# get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")
# get_ipython().run_line_magic('matplotlib', 'inline')
# In[2]:
# # Loading Data
# In[3]:

base_dir = path_config.base_dir
train_dir = path_config.train_dir
train_txt = path_config.train_txt

test_txt = path_config.test_txt
val_txt = path_config.val_txt
vocab_txt = path_config.vocab_txt

save_path = path_config.save_path

seged_clf_path = path_config.seged_clf_path
tensorboard_dir = path_config.tensorboard_dir

# In[4]:


# define local file names
test_data_file_name = test_txt
train_data_file_name = train_txt
val_data_file_name = val_txt
vocab_data_file_name = vocab_txt

# In[5]:


train_dir

# # Prepare Data

# In[6]:


test_data_df = pd.read_fwf(test_data_file_name, header=None, delimiter="\t", quoting=0, encoding='utf-8')
test_data_df.columns = ["Categories", "Text"]

# In[7]:


train_data_df = pd.read_fwf(train_data_file_name, header=None, delimiter="\t", quoting=0, encoding='utf-8')
train_data_df.columns = ["Categories", "Text"]

# In[8]:


val_data_df = pd.read_fwf(val_data_file_name, header=None, delimiter="\t", quoting=0, encoding='utf-8')
val_data_df.columns = ["Categories", "Text"]

# In[ ]:


# In[9]:


train_data_df.Categories.value_counts()

# In[10]:


import numpy as np

np.max([len(s.split(" ")) for s in train_data_df.Text])

# In[ ]:


# In[11]:


## 对数据集的标签数据进行编码
train_y = train_data_df.Categories
val_y = val_data_df.Categories
test_y = test_data_df.Categories
le = LabelEncoder()
train_y = le.fit_transform(train_y).reshape(-1, 1)
val_y = le.transform(val_y).reshape(-1, 1)
test_y = le.transform(test_y).reshape(-1, 1)

## 对数据集的标签数据进行one-hot编码
ohe = OneHotEncoder()
train_y = ohe.fit_transform(train_y).toarray()
val_y = ohe.transform(val_y).toarray()
test_y = ohe.transform(test_y).toarray()

# In[12]:


max_words = 200000
max_len = 210
tok = Tokenizer(num_words=max_words)
tok.fit_on_texts(train_data_df.Text)

## 使用word_index属性可以看到每次词对应的编码
## 使用word_counts属性可以看到每个词对应的频数
for ii, iterm in enumerate(tok.word_index.items()):
    if ii < 10:
        print(iterm)
    else:
        break
print("===================")
for ii, iterm in enumerate(tok.word_counts.items()):
    if ii < 10:
        print(iterm)
    else:
        break

# In[13]:


tok.word_index.items()

# In[14]:


## 对每个词编码之后，每句新闻中的每个词就可以用对应的编码表示，即每条新闻可以转变成一个向量了：
train_seq = tok.texts_to_sequences(train_data_df.Text)
val_seq = tok.texts_to_sequences(val_data_df.Text)
test_seq = tok.texts_to_sequences(test_data_df.Text)
## 将每个序列调整为相同的长度
train_seq_mat = sequence.pad_sequences(train_seq, maxlen=max_len)
val_seq_mat = sequence.pad_sequences(val_seq, maxlen=max_len)
test_seq_mat = sequence.pad_sequences(test_seq, maxlen=max_len)

print(train_seq_mat.shape)
print(val_seq_mat.shape)
print(test_seq_mat.shape)

# In[ ]:


# In[17]:


## 定义LSTM模型
inputs = Input(name='inputs', shape=[max_len])
## Embedding(词汇表大小,batch大小)
layer = Embedding(max_words + 1, 128, input_length=max_len)(inputs)
layer = LSTM(128)(layer)
layer = Dense(128, activation="relu", name="FC1")(layer)
layer = Dropout(0.5)(layer)
layer = Dense(3, activation="softmax", name="FC2")(layer)
model = Model(inputs=inputs, outputs=layer)
model.summary()
model.compile(loss="categorical_crossentropy", optimizer=RMSprop(), metrics=["accuracy"])

# In[15]:


# model = tf.keras.Sequential([
#    tf.keras.layers.Embedding(max_words+1,128,input_length=max_len),
#    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(
#        128, return_sequences=True)),
#    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128)),
#    tf.keras.layers.Dense(64, activation='relu'),
#    tf.keras.layers.Dense(3, activation='sigmoid')
# )


# In[16]:


# model.compile(loss='categorical_crossentropy',
#              optimizer='adam',
#              metrics=['accuracy'])


# In[21]:


# history = model.fit(test_seq_mat,test_y,batch_size=128, epochs=6, validation_data=(val_seq_mat,val_y))


# In[ ]:


# Find the following in your keras/tensorflow_backend.py file you'll add config.gpu_options.allow_growth= True in both places
#
# if _SESSION is None:
#            if not os.environ.get('OMP_NUM_THREADS'):
#                config = tf.ConfigProto(allow_soft_placement=True)
#                config.gpu_options.allow_growth=True
#            else:
#                num_thread = int(os.environ.get('OMP_NUM_THREADS'))
#                config = tf.ConfigProto(intra_op_parallelism_threads=num_thread,
#                                        allow_soft_placement=True)
#                config.gpu_options.allow_growth=True
#            _SESSION = tf.Session(config=config)
#        session = _SESSION


# In[ ]:


history = model.fit(train_seq_mat, train_y, batch_size=128, epochs=20,
                    validation_split=0.2, callbacks=[EarlyStopping(monitor='val_loss', min_delta=0.0001)])

# In[22]:


test_loss, test_acc = model.evaluate(test_seq_mat, test_y)

print('Test Loss: {}'.format(test_loss))
print('Test Accuracy: {}'.format(test_acc))

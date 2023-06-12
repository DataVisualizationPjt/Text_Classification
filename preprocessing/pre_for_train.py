#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def preprocessing_train(x, y,stopwords=None, split=True):
    # Import Library
    import pandas as pd
    import numpy as np
    import re
    from tqdm import tqdm
    from konlpy.tag import Okt
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from sklearn.model_selection import train_test_split
    okt = Okt()

    def tokenize(text):
        tokens = okt.morphs(text)
        return tokens
    
    def combine_tokens(tokens):
        combined_tokens = []
        i = 0
        while i < len(tokens):
            if tokens[i] == '영' and i < len(tokens) - 1 and tokens[i+1].startswith('입'):
                combined_tokens.append('영입')
                if tokens[i+1] != '입':
                    combined_tokens.append(tokens[i+1][1:])
                i += 2
                continue
            combined_tokens.append(tokens[i])
            i += 1
        return combined_tokens
    
    if stopwords == None:
        with open('stopword.txt', 'r', encoding='utf-8') as file:
            stopwords = file.read().splitlines()
        
    if split == True:
        X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=0, stratify=y_data)
        
        print('--------Ratio of Train Data--------')
        print(f'Not Interested = {round(y_train.value_counts()[0]/len(y_train) * 100,3)}%')
        print(f'Interested = {round(y_train.value_counts()[1]/len(y_train) * 100,3)}%')
        
        print('--------Ratio of Test Data--------')
        print(f'Not Interested = {round(y_test.value_counts()[0]/len(y_test) * 100,3)}%')
        print(f'Interested = {round(y_test.value_counts()[1]/len(y_test) * 100,3)}%')
        
        train_test=[]
        
        for data in [X_train, X_test]:
            data = data.reset_index(drop=True)
            for idx in tqdm(range(len(data))):
                data[idx] = tokenize(data[idx])
                data[idx] = combine_tokens(data[idx])
                result = []
                for word in data[idx]: 
                    if (word not in stopwords) & (len(word)>1): 
                        result.append(word)
                data[idx] = result
            # Encoding
            tokenizer = Tokenizer()
            tokenizer.fit_on_texts(data)
            encoded_tokens = tokenizer.texts_to_sequences(data)
            # Padding
            max_len = max(len(item) for item in encoded_tokens)
            data = pad_sequences(encoded_tokens, maxlen = max_len)
            train_test.append(data)
            X_train = train_test[0]
            X_test = train_test[1]

        return X_train, X_test, y_train, y_test
        
    else:
        X_train = x
        y_train = y
        
        print('--------Ratio of Train Data--------')
        print(f'Not Interested = {round(y_train.value_counts()[0]/len(y_train) * 100,3)}%')
        print(f'Interested = {round(y_train.value_counts()[1]/len(y_train) * 100,3)}%')
        
        X_train = X_train.reset_index(drop=True)
        for idx in tqdm(range(len(X_train))):
            X_train[idx] = tokenize(X_train[idx])
            X_train[idx] = combine_tokens(X_train[idx])
            result = []
            for word in X_train[idx]: 
                if (word not in stopwords) & (len(word)>1): 
                    result.append(word)
            X_train[idx] = result
        # Encoding
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(X_train)
        encoded_tokens = tokenizer.texts_to_sequences(X_train)
        # Padding
        max_len = max(len(item) for item in encoded_tokens)
        X_train = pad_sequences(encoded_tokens, maxlen = max_len)
        
        return X_train, y_train
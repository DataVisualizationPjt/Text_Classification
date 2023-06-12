#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def preprocessing_df(df):
    # Import Library
    import pandas as pd
    import re
    from tqdm import tqdm
    
    def remove_numbers(text):
        df.loc[raw,col] = re.sub(r'\d+', '', text)  # 숫자를 공백으로 대체
        return df.strip()  # 양쪽 공백 제거
    
    def cleaning(text):
        try:
            text = text.replace('[','(')
            text = text.replace(']',')')
            text = re.sub(pattern=r'\([^)]*\)', repl='', string= text)
            text = re.sub(pattern=r'\{[^}]*\)', repl='', string= text)
            text = re.sub(pattern=r'\<[^>]*\)', repl='', string= text)
        except:
            pass
        try:
            text = re.sub(pattern=r'[^ 가-힣a-zA-Z0-9_]', repl='', string= text)
        except:
            pass
    
    df = df.dropna()
    df = df.reset_index(drop=True)
    for raw in tqdm(range(len(df))):
        for col in ['title','article']:
            df.loc[raw,col] = remove_numbers(df.loc[raw,col])
            df.loc[raw,col] = cleaning(df.loc[raw,col])
            
    return df


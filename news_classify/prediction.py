#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def prediction(model_path):
    # Import Library
    import pandas as pd
    import selenium
    import time
    from tqdm import tqdm
    import random as rd
    from datetime import datetime
    import tensorflow as tf

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    import pyperclip

    from news_classify.pre_for_df import preprocessing_df as pre_df
    from news_classify.pre_for_train import preprocessing_train as pre_train
    
    def crawling():
        print('Crawling Today News..')
        sports_news = {'news':[]}

        driver = webdriver.Chrome()
        driver.get('https://www.naver.com/')
        driver.maximize_window()
        time.sleep(rd.uniform(0.3,1))

        driver.find_element(By.CSS_SELECTOR,r'#account > div > a').click()
        time.sleep(rd.uniform(0.3,1))

        # Log In
        # user_id = str(input('아이디를 입력하세요: '))
        # user_passwd = str(input('비밀번호를 입력하세요: '))
        user_id = 'sysconan'
        user_passwd = '!Brandan0211'

        driver.find_element(By.CSS_SELECTOR,r'#id_line').click()
        pyperclip.copy(user_id)
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        time.sleep(rd.uniform(0.3,1))

        driver.find_element(By.CSS_SELECTOR,r'#pw').click()
        pyperclip.copy(user_passwd)
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        time.sleep(rd.uniform(0.3,1))

        driver.find_element(By.CSS_SELECTOR,r'#log\.login').click()
        time.sleep(rd.uniform(2,2.5))

        # Go To Sports Page
        driver.execute_script("window.scrollTo(300, 0);")
        driver.find_element(By.CSS_SELECTOR,r'#shortcutArea > ul > li:nth-child(10) > a').click()
        driver.find_element(By.CSS_SELECTOR,r'#shortcutArea > div > ul > li:nth-child(9) > a').click()
        time.sleep(rd.uniform(0.3,1))
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element(By.CSS_SELECTOR,r'#lnb_list > li:nth-child(13) > a').click()
        time.sleep(rd.uniform(1,1.5))
        
        #-----------------------------------------
#         driver.find_element(By.CSS_SELECTOR,r'a.arr.prev').click()
#         time.sleep(rd.uniform(1,1.5))
        #-----------------------------------------

        start = time.time()

        # Crawling Titles, Articles, Interested
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        news_lst = driver.find_elements(By.CSS_SELECTOR, 'div#_newsList > ul > li > div.text')
        date = driver.find_element(By.CSS_SELECTOR,'span.day').text[:10]
        for news in tqdm(range(len(news_lst))):
            try:
                driver.find_element(By.CSS_SELECTOR,
                                    f'div#_newsList > ul > li:nth-child({news+1}) > div.text > a').click()
                title = driver.find_element(By.CSS_SELECTOR,'h4.title').text
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                article = driver.find_element(By.CSS_SELECTOR,'div#newsEndContents').text
                article = article.replace('\n','')

                # Delete Unnecessary Elements
                for div in driver.find_elements(By.CSS_SELECTOR,'div#newsEndContents > div'):
                    article = article.replace(div.text,'')

                for p in driver.find_elements(By.CSS_SELECTOR,'div#newsEndContents > p'):
                    article = article.replace(p.text,'')

                for em in driver.find_elements(By.CSS_SELECTOR,'div#newsEndContents > span > em'):
                    article = article.replace(em.text,'')

                for td in driver.find_elements(By.CSS_SELECTOR,
                                               'div#newsEndContents > font > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td'):
                    article = article.replace(td.text,'')

                if driver.find_element(By.CSS_SELECTOR,
                                       '#__markup_tomain > div > a').get_attribute('aria-pressed') == 'true':
                    interested = 1
                else:
                    interested = 0

                sports_news['news'].append({'date':date,
                                           'title':title,
                                           'article':article,
                                           'interested':interested,
                                           'link':str(driver.current_url)})

            except:
                pass

            driver.back()
            time.sleep(rd.uniform(0.3,0.5))

        print(f"time : {time.time() - start}s")
        driver.quit()
        
        df = pd.DataFrame(sports_news['news'])
        
        return df
    
    def preprocessing(df):
        for raw in range(len(df)):
            df.loc[raw,'date'] = df.loc[raw,'date'].replace('.','-')
            df.loc[raw,'date'] = datetime.strptime(df.loc[raw,'date'],'%Y-%m-%d')
            
        df1 = df.copy()
        df1 = pre_df(df1)
        x_pred, y_pred = pre_train(df1['title'],df1['interested'], split=False)
        
        return x_pred, y_pred
    
    def predicting(x_pred, model_path):
        model = tf.keras.models.load_model(model_path)
        score = model.predict(x_pred)
        score = score.astype('float')
        
        target = []
        for i in score:
            target.append(float(i))
            
        return target
            
    df = crawling()
    x_pred, y_pred = preprocessing(df)
    target = predicting(x_pred, model_path)
    
    df['interested'] = target
    
    return df
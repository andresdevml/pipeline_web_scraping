
# importamos algunas cosas 

import pandas as pd 
import nltk
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
from urllib.parse import urlparse
import hashlib

# definimos las funciones a usar 

def tokenize_column(df,column_name,name_token):

    stop_words = set(stopwords.words('spanish'))

    column=df[column_name]

    column=column.apply(lambda row: row.lower())

    column=column.apply(lambda row: nltk.word_tokenize(row))

    column=column.apply(lambda list_tokens: 
                        list(filter(
                            lambda token: token.isalpha(),
                                                list_tokens)))
    column=column.apply(lambda word_list: 
                        list(filter(lambda word: 
                                    word not in stop_words, 
                                    word_list)))
    
    column=column.apply(lambda valid_word_list: len(valid_word_list))

    df[name_token]=column

    return df


def create_id(df,column_name):
    # column_name provide a key for the hash

    column=df[column_name]

    column=column.apply(lambda row: 
                    hashlib.md5(bytes(row.encode() ) ) )
    
    column=column.apply(lambda hash_object: hash_object.hexdigest())

    df['id'] = column
    
    df.set_index('id', inplace=True)

    return df 


def append_name_host(df,name_news_paper,url_news_paper):

    df['host']=url_news_paper

    df['Name news paper']=name_news_paper

    return df 
    
    
    
    
if __name__=='__main__':
	
	url = 'https://elestimulo.com/'
	
	df=pd.read_csv('data_web_el_estimulo.csv')

	df=tokenize_column(df,'Title','Num of words in title')

	df=tokenize_column(df,'Content','Num of words in content')

	df=create_id(df,'Hiper Link')

	df=append_name_host(df,'elestimulo',url)

	df.to_csv('proces_data_elestimulo.csv',index=True)
	
	print('\n\n Culmino el wraling \n\n')

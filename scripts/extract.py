import requests
import bs4 
import re
import pandas as pd 
from datetime import datetime

# filtra los links que no tengan articulos
# regresa una lista con todos los links :

def article_verification(list_href):

    url = 'https://elestimulo.com/'

    list_articles=[]

    for href in list_href:

        article_url=url+href

        article_page=requests.get(article_url)

        article_soup=bs4.BeautifulSoup(article_page.content,
                                       'html.parser')
        
        title=len(article_soup.find_all('h1',
                                      class_='ArticleTitle_1ARzk'))
   
        description=len(article_soup.find_all('p',
                                    class_='ArticleDescription_2mEsZ'))
        
        content=len(article_soup.find_all('div',
                                    class_='ArticleContent_19ZsC'))
        
        if (content and description and title):

            list_articles.append(article_url)

    return list_articles


# Extraemos los titulos de los links de los articulos
# regresa una lista con todos los titulos :

def extract_titles(list_articles):

    titles=[]

    for link in list_articles:

        page=requests.get(link)

        soup=bs4.BeautifulSoup(page.content,'html.parser')

        title=soup.find_all('h1',
                    class_='ArticleTitle_1ARzk')[0].text

        titles.append(title)

    return titles


# Extrae el contenido del articulo. Solamente los parrafos. Ignora
# titulos, twits y otros recursos.
# regresa una lista donde cada elemento es un string con todo el
# contenido del articulo.

def extract_contents(list_articles):

    bag_of_contents=[]

    for link in list_articles:

        text_thread=''

        space=' '

        page=requests.get(link)

        soup=bs4.BeautifulSoup(page.content,'html.parser')

        description=soup.find_all('p',
                            class_='ArticleDescription_2mEsZ')[0].text

        text_thread= text_thread + description

        content=soup.find_all('div',
                            class_='WPContent ArticleInner_8P9AV')[0]
        
        paragraphs=content.find_all('p')

        for paragraph in paragraphs :

            cond_1=(len(paragraph.contents)==1)

            cond_2=(len(paragraph.attrs)==0)

            if cond_1 and cond_2 :

                text_thread=text_thread+space+paragraph.text

        bag_of_contents.append(text_thread)

    return bag_of_contents



if __name__=='__main__':
	
	
	    # primero extraemos las referencias 

	url = 'https://elestimulo.com/'

	page=requests.get(url)

	soup=bs4.BeautifulSoup(page.content,'html.parser')

    #tenemos la sopa. Vamos a buscar las etiquetas de interes 

	dict={'class':None ,'href':re.compile('-')} # filtro de la busqueda

	branch_news_principal_page=soup.find_all('a',attrs=dict)

	list_href_no_unique=[ selector['href'] for selector in 
                                branch_news_principal_page] # ponemos todas las
                                                            # referencias en una 
                                                            # lista

	list_href=list(set(list_href_no_unique)) # eliminamos las referencias repetidas 


	try:
		list_href.remove('/video-home/')
	except:
		pass

	try:
		list_href.remove('/vivoplay-en-vivo/')
	except:
		pass

# Eliminamos estos links que no van a ningun sitio relevante
	
# aplicamos las funciones

	list_articles=article_verification(list_href)

	list_titles=extract_titles(list_articles)

	list_contents=extract_contents(list_articles)


# Finalmente organizmos en una lista que contiene 

	portal_news=list(zip(list_articles,list_titles,list_contents))


# los guardamos en un csv a traves de pandas :


	data_web= pd.DataFrame(portal_news,
                  columns =['Hiper Link', 'Title','Content'])

# exportamos el csv 

	

	data_web.to_csv('data_web_el_estimulo.csv',index=False)
	
	print('\n\n Culmino el scraping \n\n')

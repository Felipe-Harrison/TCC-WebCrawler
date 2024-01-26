import requests
from bs4 import BeautifulSoup
from datetime import datetime
from Crawler import Crawler,PageData
from time import time as now

# body {"variables":{"page":2,"perPage":100,"hat":"verificação"},"query":"query ($perPage: Int, $hat: String, $page: Int) {\n  NewsItems(\n    first_published_at_lt: \"2024-01-23T19:03:32.954Z\"\n    page: $page\n    per_page: $perPage\n    sort_by: \"first_published_at:desc\"\n    filter_query_v2: {hat: {in: $hat}}\n  ) {\n    total\n    items {\n      full_slug\n      uuid\n      first_published_at\n      name\n      content {\n        hat\n        custom_hat\n        featured_title\n        featured_image {\n          filename\n          __typename\n        }\n        resume\n        authors {\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"}

# https://gapi.storyblok.com/v1/api
# Headers token: S4otl4itHUavEuIIbVlrrgtt

class LupaCrawler(Crawler):
    # Pegar lista de noticias
    def getNoticias(self,page:BeautifulSoup) -> list:
        noticias = []
        noticias_block = page.findAll('div',attrs={'class':'sc-hLBbgP eQMdjh'})
        if len(noticias_block) > 0:
            noticias = noticias_block[2].findAll('',attrs={'':''})
        return noticias
    
    # Procurar proxima pagina
    def getNextPage(self,page:BeautifulSoup):
        nextLink = page.find('a', attrs={'class': ''})
        if nextLink != None:
            self.urls.append(nextLink['href'])
    
    # Pegar dados da noticia
    def getDataFromNoticia(self,noticia:BeautifulSoup) -> PageData:
        try:
            titulo = noticia.find("",attrs={'': ''})
            url = titulo.a.get('href')
            titulo_text = titulo.a.get_text()
            
            datapublicaco = noticia.find('time',attrs={'class': "entry-date published"})
            data_datetime = datetime.fromisoformat(datapublicaco['datetime'])
            # = self.getDataFromUrl(url)
            
            return PageData(
                url=url,
                titulo=titulo_text,
                dataPublicacao=data_datetime,
                categorias=[],
                conclusao="",
                texto=""
            )
            
        except:
            print("Error in: ",url)
            return None
    
    # Pegar dados da pagina da noticia
    def getDatafromPage(self,page:BeautifulSoup):
        texto_block = page.find('div',attrs={'class': "nv-content-wrap entry-content"}).findAll(['p','h2'])
        texto_limpo = ' '.join(texto.get_text() for texto in texto_block)
        
        return conclusao,texto

if __name__ == "__main__":
    urls = [
        "https://lupa.uol.com.br/jornalismo/categoria/verifica%C3%A7%C3%A3o"
    ]
    tempoInicio = now()
    try:   
        modelo = LupaCrawler(urlsIniciais=urls,arquivo="lupa")
        modelo.scrape()
        
    except requests.ConnectTimeout:
        print("Erro de timeout")
        
    except KeyboardInterrupt:
        pass
    
    finally:
        print("Tempo gasto Total: ",f"{(now() - tempoInicio):.2f}s")
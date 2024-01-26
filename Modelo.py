import requests
from bs4 import BeautifulSoup
from datetime import datetime
from Crawler import Crawler,PageData
from time import time as now

class Modelo(Crawler):
    # Pegar lista de noticias
    def getNoticias(self,page:BeautifulSoup) -> list:
        noticias = []
        noticias_block = page.find('',attrs={'':''})
        if noticias_block != None:
            noticias = noticias_block.findAll('',attrs={'':''})
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
    urls = []
    tempoInicio = now()
    try:   
        modelo = Modelo(urlsIniciais=urls,arquivo="modelo")
        modelo.scrape()
        
    except requests.ConnectTimeout:
        print("Erro de timeout")
        
    except KeyboardInterrupt:
        pass
    
    finally:
        print("Tempo gasto Total: ",f"{(now() - tempoInicio):.2f}s")
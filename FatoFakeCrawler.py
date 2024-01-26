import requests
from bs4 import BeautifulSoup
from datetime import datetime
from Crawler import Crawler,PageData
from time import time as now

class FatoFakeCrawler(Crawler):
    # Pegar lista de noticias
    def getNoticias(self,page:BeautifulSoup) -> list:
        noticias = []
        noticias_block = page.find('div',attrs={'class': "_evg"})
        if noticias_block != None:
            noticias = noticias_block.findAll('div',attrs={'class': "feed-post-body"})
        return noticias
    
    # Procurar proxima pagina
    def getNextPage(self,page:BeautifulSoup):
        nextLink = page.find('div', attrs={'class': 'load-more gui-color-primary-bg'})
        if nextLink != None:
            self.urls.append(nextLink.a['href'])
    
    # Pegar dados da noticia
    def getDataFromNoticia(self,noticia:BeautifulSoup) -> PageData:
        try:
            titulo = noticia.find('h2')
            url = titulo.a.get('href')
            titulo_text = titulo.a.p.getText()
            
            texto,conclusao,data_datetime = self.getDataFromUrl(url)
            
            if titulo_text.find("#FAKE"):
                categorias = ["Falso"]
            elif titulo_text.find("#FATO"):
                categorias = ["Verdadeiro"]
            else:
                categorias = []
            
            return PageData(
                url=url,
                titulo=titulo_text,
                dataPublicacao=data_datetime,
                categorias=categorias,
                conclusao=conclusao,
                texto=texto
            )
            
        except:
            print("Error in: ",url)
            return None
    
    # Pegar dados da pagina da noticia
    def getDatafromPage(self,page:BeautifulSoup):
        conclusao = page.find('h2',attrs={'class': 'content-head__subtitle'}).get_text()
        datapublicaco = page.find('time',attrs={'itemprop': "datePublished"})
        data_datetime = datetime.fromisoformat(datapublicaco['datetime'])
        
        # Pegar texto e conslusao
        texto_block = page.find('article',attrs={'itemprop': "articleBody"}).findAll(['p','h2'])
        texto_limpo = ' '.join(texto.get_text() for texto in texto_block)
        
        return texto_limpo,conclusao,data_datetime

if __name__ == "__main__":
    urls = [
        "https://g1.globo.com/fato-ou-fake/",
    ]
    tempoInicio = now()
    try:   
        modelo = FatoFakeCrawler(urlsIniciais=urls,arquivo="fatofake")
        modelo.scrape()
        
    except requests.ConnectTimeout:
        print("Erro de timeout")
        
    except KeyboardInterrupt:
        pass
    
    finally:
        print("Tempo gasto Total: ",f"{(now() - tempoInicio):.2f}s")

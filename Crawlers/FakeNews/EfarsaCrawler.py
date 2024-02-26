import requests
from bs4 import BeautifulSoup
from datetime import datetime
from Crawlers.Crawler import Crawler,PageData
from time import time as now

class EfarsaCrawler(Crawler):
    # Pegar lista de noticias
    def getNoticias(self,page:BeautifulSoup) -> list:
        noticias = []
        noticias_block = page.find('div',attrs={'class': "td_block_inner tdb-block-inner td-fix-index"})
        if noticias_block != None:
            noticias = noticias_block.findAll('div',attrs={'class': "td-module-container td-category-pos-above"})
        return noticias
    
    # Procurar proxima pagina
    def getNextPage(self,page:BeautifulSoup):
        nextLink = page.find('a', attrs={'aria-label': 'next-page'})
        if nextLink != None:
            self.urls.append(nextLink['href'])
    
    # Pegar dados da noticia
    def getDataFromNoticia(self,noticia:BeautifulSoup) -> PageData:
        try:
            
            datapublicaco = noticia.find('time',attrs={'class': "entry-date updated td-module-date"})
            titulo = noticia.find('h3',attrs={'class': "entry-title td-module-title"})
            data_datetime = datetime.fromisoformat(datapublicaco['datetime'])
            
            url = titulo.a.get('href')
            
            texto,conclusao,categorias = self.getDataFromUrl(url)
        
            return PageData(
                url=url,
                titulo=titulo.get_text(),
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
        
        NOTICIA_TEXTO = "div.td_block_wrap.tdb_single_content.tdi_99.td-pb-border-top.td_block_template_1.td-post-content.tagdiv-type > div" #div
        
        texto_block = page.select(NOTICIA_TEXTO)[0].findAll(['p','h2'])
        texto_limpo = ' '.join(texto.get_text() for texto in texto_block)
        
        if "Conclusão" in texto_limpo:
            texto, conclusao = texto_limpo.split("Conclusão")
        else:
            texto = texto_limpo
            conclusao = ""
        
        # Pegar categorias
        categorias_div = page.find('div', attrs={'class': "tdb-category td-fix-index" })
        if categorias_div != None:
            categorias_lista = categorias_div.findAll('a')
            categorias = [categoriaA.get_text() for categoriaA in categorias_lista]
        else:
            categorias = []
        
        return texto,conclusao,categorias

if __name__ == "__main__":
    urls = [
        "https://www.e-farsas.com/secoes/falso-2",
    ]
    tempoInicio = now()
    try:   
        modelo = EfarsaCrawler(urlsIniciais=urls,arquivo="efarsa")
        modelo.scrape()
        
    except requests.ConnectTimeout:
        print("Erro de timeout")
        
    except KeyboardInterrupt:
        pass
    
    finally:
        print("Tempo gasto Total: ",f"{(now() - tempoInicio):.2f}s")

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from Crawlers.Crawler import Crawler,PageData,makeRequest
from time import time as now
import json

def getText(bs4obj,tag,attrs):
    auxBlock = bs4obj.find(tag,attrs=attrs)
    text = ""
    if auxBlock != None:
        text = auxBlock.get_text() 
    return text

def limpaUrl(url):
    if str(url).endswith('/'):
        return url[:-1]
    return url

class FolhaCrawler(Crawler):
    
    def __init__(self, urlsIniciais: list, arquivo: str = 'placeholder') -> None:
        super().__init__(urlsIniciais, arquivo)
        self.noticias = []
    
    # Pegar lista de noticias
    def getNoticias(self,page:BeautifulSoup) -> list:
        noticias = []
        noticias_block = page.findAll('ol',attrs={'class':'u-list-unstyled'})[1]
        if noticias_block != None:
            noticias = noticias_block.findAll('div',attrs={'class':'c-headline__content'})
            for noticia in noticias:
                link = noticia.find('a')
                self.noticias.append(link.get('href'))
    
    # Procurar proxima pagina
    def getNextPage(self,page:BeautifulSoup):
        pass
        # nextLink = page.find('a', attrs={'class': ''})
        # if nextLink != None:
        #     self.urls.append(nextLink['href'])
    
    # Pegar dados da noticia
    def getDataFromNoticia(self,noticia:str) -> PageData:
        
        try:
            url = noticia
            titulo,conclusao,categoria,texto,data = self.getDataFromUrl(url)
            
            return PageData(
                url=url,
                titulo=titulo,
                dataPublicacao=data,
                categorias=categoria,
                conclusao=conclusao,
                texto=texto
            )
            
        except Exception as e:
            print("Error in: ",url,e)
            return None
    
    # Pegar dados da pagina da noticia
    def getDatafromPage(self,page:BeautifulSoup):
        
        # Definer se noticia paga ou gratis
        contentClassSelectors = [
            {
                'type': 1, # gratis
                'classText': "j-paywall news__content js-news-content js-disable-copy"
            },
            {
                'type': 0, # paga
                'classText':"container j-paywall"
            },
        ]
        
        tipoNoticia = 0
        texto_block = []
        
        for classSelector in contentClassSelectors:
            content = page.find('div',attrs={'class':classSelector['classText']})
            if content != None:
                tipoNoticia = classSelector['type']
                texto_block = content.findAll(['p'])
                break

        # Noticia paga
        if tipoNoticia == 0:
            headerBlock = page.find('div',attrs={'class':"c-content-head__wrap"})
            titulo = getText(headerBlock,'h1',attrs={'class':"c-content-head__title"})
            conclusao = getText(headerBlock,'h2',attrs={'class':"c-content-head__subtitle"})
            categoria = getText(headerBlock,'span',attrs={'class':"c-labels__item"})
            # buscar novos links
            linksBlock = page.find('ul',attrs={'class':"c-newslist c-newslist--no-gap"})
            links = []
            if linksBlock != None:
                links = linksBlock.findAll(['li'])
            for link in links:
                newLink = link.find('a')
                self.noticias.append(limpaUrl(newLink.get('href')))
        else:
            titulo = getText(page,'h1',attrs={'class':"news__title"})
            conclusao = getText(page,'p',attrs={'class':"news__subtitle"})
            categoria = getText(page,'a',attrs={'class':"section-title section-title__return"})
            # buscar novos links
            linksBlock = page.findAll('li',attrs={'class':"read-more__item"})
            for link in linksBlock:
                newLink = link.find('a')
                self.noticias.append(limpaUrl(newLink.get('href')))
            
        texto_limpo = ' '.join(texto.get_text() for texto in texto_block)
        
        datapublicaco = page.find('time',attrs={'class': "c-more-options__published-date"})
        data = datapublicaco['datetime'] if datapublicaco['datetime'] != "#" else str(datetime.now())
        data_datetime = datetime.fromisoformat(data)
        
        return titulo,conclusao,[categoria],texto_limpo,data_datetime
    
    def scrape(self):

        totalData = 0
        # Enquanto tiver links para visitar
        while len(self.urls) != 0:
            
            # Feedback/Analise
            data = []
            dataPage = 100
            
            tempoInicioPagina = now()
            print("Pagina: ",self.urls[0])
            
            # Pegar página do primeiro link disponivel
            site = makeRequest(url=self.urls[0])
            
            # Procurar por todas as noticias na url atual
            self.getNoticias(site)
            
            # Enquanto tiver noticia -> buscar dados
            while len(self.noticias) != 0:
                
                pageData = self.getDataFromNoticia(self.noticias[0])
                if pageData != None:
                    data.append(pageData.getData())

                if len(data) >= dataPage:
                    # Salvar as noticias encontradas ate o momento
                    with open(f"Resultados/{self.arquivo}_data.json",'a+',encoding="utf8") as f:
                        json.dump(data,f,indent=4,allow_nan=True,ensure_ascii = False)
                        totalData += len(data)
                        print(f"Noticas salvas até o momento: {totalData}")
                        data = []
                        f.close()
                    print("Tempo gasto: ",f"{(now() - tempoInicioPagina):.2f}s")
                    tempoInicioPagina = now()
                # Remover link atual
                self.noticias.pop(0)
            
            self.urls.pop(0)
        
        # end while

if __name__ == "__main__":
    urls = [
        "https://www1.folha.uol.com.br/ultimas-noticias/#100"
    ]

    tempoInicio = now()
    try:   
        modelo = FolhaCrawler(urlsIniciais=urls,arquivo="folhasp")
        modelo.scrape()
        
    except requests.ConnectTimeout:
        print("Erro de timeout")
        
    except KeyboardInterrupt:
        pass
    
    finally:
        print("Tempo gasto Total: ",f"{(now() - tempoInicio):.2f}s")
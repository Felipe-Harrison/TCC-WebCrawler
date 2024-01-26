import requests
from bs4 import BeautifulSoup
import json
from time import time as now

def makeRequest(url) -> BeautifulSoup:
    response = requests.get(url=url)
    content = response.content
    return BeautifulSoup(content,'html.parser')

class PageData:
    def __init__(self,url,titulo,dataPublicacao,categorias,conclusao,texto) -> None:
        self.url  = url
        self.titulo = titulo
        self.datapublicacao = str(dataPublicacao)
        self.categorias = categorias
        self.conclusao = conclusao
        self.texto = texto
    
    def getData(self) -> dict:
        return {
            'url': self.url,
            'titulo': self.titulo,
            'data-publicacao': self.datapublicacao,
            'categorias': self.categorias,
            'conclusao': self.conclusao,
            'rotulo': '',
            'texto': self.texto,
        }
    
class Crawler:
    
    def __init__(self,urlsIniciais:list,arquivo:str='placeholder') -> None:
        self.urls = urlsIniciais
        self.arquivo = arquivo
        
    # Pegar lista de noticias
    def getNoticias(page) -> list:
        pass
    
    # Procurar proxima pagina
    def getNextPage(self,page):
        pass
    
    # Pegar dados da noticia
    def getDataFromNoticia(self,noticia) -> PageData:
        #self.getDataFromUrl(url)
        pass
    
    # Pegar dados da pagina da noticia
    def getDatafromPage(page):
        pass

    def getDataFromUrl(self,url):
        """
        Returns:
            Elementos que forem retornados em getDataFromPage
        """
        paginaNoticia = makeRequest(url)
        return self.getDatafromPage(page=paginaNoticia)
    
    def scrape(self):

        totalData = 0
        # Enquanto tiver links para visitar
        while len(self.urls) != 0:
            
            # Feedback/Analise
            data = []
            dataPage = 0
            
            tempoInicioPagina = now()
            print("Pagina: ",self.urls[0])
            
            # Pegar página do primeiro link disponivel
            site = makeRequest(url=self.urls[0])
            
            # Procurar por todas as noticias na url atual
            noticias = self.getNoticias(site)

            # Procurar nova página
            self.getNextPage(site)
            
            dataPage = len(noticias)
            # Para cada noticia encontrada buscar dados
            for noticia in noticias:
                
                pageData = self.getDataFromNoticia(noticia)
                if pageData != None:
                    data.append(pageData.getData())
            
            # Salvar as noticias encontradas ate o momento
            with open(f"Resultados/{self.arquivo}_data.json",'a+',encoding="utf8") as f:
                json.dump(data,f,indent=4,allow_nan=True,ensure_ascii = False)
                totalData += len(data)
                print(f"Noticas salvas até o momento: {totalData}, nessa pagina: {len(data)}/{dataPage}")
                f.close() 
            
            print("Tempo gasto: ",f"{(now() - tempoInicioPagina):.2f}s")
            # Remover link atual
            self.urls.pop(0)
        
        # end while

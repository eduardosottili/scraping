import requests
from bs4 import BeautifulSoup
import mysql.connector 
from datetime import datetime
import schedule
import time

conexao = mysql.connector.connect(
    host='localhost',
    port=3307,
    user='root',
    password='root',
    database='dbmercadolivre',
)
cursor = conexao.cursor()
#web scraping
def obtem_produto():
    try:
        # Web scraping
        link = "https://produto.mercadolivre.com.br/MLB-3769888085-mouse-sem-fio-_JM"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
        requisicao = requests.get(link, headers=headers)
        site = BeautifulSoup(requisicao.text, "html.parser")

        titulo = site.find("h1", class_="ui-pdp-title")
        if titulo is not None:
            titulo = titulo.text.strip()
            print('Título do produto: ', titulo)
        else:
            titulo = "Título não encontrado"
        
        
        valor_produto = site.find("span", class_="andes-money-amount__fraction")
        if valor_produto is not None:
            valor_text = valor_produto.get_text()
            valor_text = valor_text.replace('.', '')  # Remover pontos dos milhares
            valor_float = float(valor_text)
            print('Valor:', valor_float)
        else:
            valor_float = 0.0
            print('Valor não encontrado')

        # Pegar a data atual
        data = lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insert no banco do valor e data
        comando = f"INSERT INTO produto (value, date, title) VALUES ({valor_float}, '{data()}', '{titulo}')"
        cursor.execute(comando)
        conexao.commit() # Sempre que editar o BD
        
        print(f"{cursor.rowcount} registro(s) inserido(s). Valor do produto: R$ {valor_float:.2f} - Data: {data()}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Agendando a tarefa para ser executada a cada minuto
schedule.every(5).seconds.do(obtem_produto)

# Mantendo o script em execução
while True:
    schedule.run_pending()
    time.sleep(1)

    #fecha conexao com o BD
    #cursor.close()
    #conexao.close()
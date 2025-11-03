# app.py
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

# URL alvo fixada (pode ser passada como parâmetro, mas vamos fixar por simplicidade)
URL_PRODUTO = "https://www.centauro.com.br/bermuda-masculina-oxer-elastic-984818.html?cor=02"

# Headers robustos para tentar evitar o 403 (ajuste se necessário)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.9',
    'Referer': 'https://www.centauro.com.br/' 
}

# ----------------------------------------------------
# Lógica de Scraping (Reaproveitando a melhor tentativa)
# ----------------------------------------------------

def extrair_conteudo_centauro(url, headers):
    """
    Acessa a URL e tenta extrair informações do produto com headers robustos.
    A lógica de cookies de sessão foi removida para simplificar a hospedagem,
    mas pode ser reintroduzida se o Render permitir.
    """
    try:
        # Tenta a requisição diretamente com headers robustos
        resposta = requests.get(url, headers=headers, timeout=20)
        resposta.raise_for_status() # Levanta erro para 4xx ou 5xx
        
        soup = BeautifulSoup(resposta.content, 'html.parser')
        
        # Tentativas de extração de dados (simplificadas)
        titulo_tag = soup.find('title')
        nome_produto = soup.find('h1') 
        preco_element = soup.find('span', class_='centauro-product-price-2-x-sellingPrice') 
        
        dados = {
            'status': 'sucesso',
            'titulo_pagina': titulo_tag.text.strip() if titulo_tag else 'Não encontrado',
            'nome_produto': nome_produto.text.strip() if nome_produto else 'Não encontrado',
            'preco_venda': preco_element.get_text(strip=True) if preco_element else 'Não encontrado',
        }
        return dados

    except requests.exceptions.HTTPError as e:
        # Se falhar (ex: 403), retorna o erro
        return {
            'status': 'erro',
            'mensagem': f"Falha HTTP. Status: {e.response.status_code}. O site pode ter bloqueado o scraper.",
            'detalhe': str(e)
        }
    except Exception as e:
        return {
            'status': 'erro',
            'mensagem': f"Erro na conexão ou na análise do HTML: {str(e)}",
            'detalhe': str(e)
        }

# ----------------------------------------------------
# ROTA API (Onde o Render vai expor o serviço)
# ----------------------------------------------------

@app.route('/')
def get_produto_info():
    """
    Rota principal que executa o scraping e retorna os dados em JSON.
    """
    dados = extrair_conteudo_centauro(URL_PRODUTO, HEADERS)
    
    # Flask/Render espera que a resposta seja JSON
    return jsonify(dados)

if __name__ == '__main__':
    # Esta parte é para rodar localmente, mas o Render usará o Gunicorn/Start Command
    app.run(debug=True)

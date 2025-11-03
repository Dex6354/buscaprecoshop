import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Configurações
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PRODUTOS = [
    {
        "nome": "Bermuda Oxer Training 7",
        "url": "https://www.centauro.com.br/bermuda-masculina-oxer-training-7-tecido-plano-981429.html?cor=02",
        "alvo": 50.0
    },
    {
        "nome": "Bermuda Oxer Elastic",
        "url": "https://www.centauro.com.br/bermuda-masculina-oxer-elastic-984818.html?cor=02",
        "alvo": 50.0
    }
]

INTERVALO = 3600  # 1 hora


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_preco(driver, url):
    driver.get(url)
    time.sleep(5)  # aguarda carregamento JS
    try:
        # Tenta localizar o preço pelo seletor do site
        preco_elem = driver.find_element(By.CSS_SELECTOR, "div.ProductPrice-value, span.Price, strong[data-testid='price-value']")
        preco_texto = preco_elem.text.strip()
        preco_texto = preco_texto.replace("R$", "").replace(".", "").replace(",", ".")
        return float(preco_texto)
    except Exception:
        return None


def enviar(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )


def verificar(driver):
    for p in PRODUTOS:
        preco = get_preco(driver, p["url"])
        if preco:
            print(f"{p['nome']}: R$ {preco:.2f}")
            if preco <= p["alvo"]:
                enviar(f"🔥 {p['nome']} está por R$ {preco:.2f}!\n{p['url']}")
        else:
            print(f"❌ Não consegui ler o preço de {p['nome']}")


if __name__ == "__main__":
    driver = setup_driver()
    enviar("🤖 Bot de monitoramento da Centauro iniciado com sucesso!")
    while True:
        verificar(driver)
        print("Aguardando próxima checagem...")
        time.sleep(INTERVALO)

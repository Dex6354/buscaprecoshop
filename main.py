from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests, time, os

# === CONFIGURAÇÕES ===
PRODUTOS = [
    {
        "nome": "Bermuda Oxer Training 7",
        "url": "https://www.centauro.com.br/bermuda-masculina-oxer-training-7-tecido-plano-981429.html?cor=02",
        "alvo": 45.0,
    },
    {
        "nome": "Bermuda Oxer Elastic",
        "url": "https://www.centauro.com.br/bermuda-masculina-oxer-elastic-984818.html?cor=02",
        "alvo": 45.0,
    },
]

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
INTERVALO = 1800  # 30 min

# === FUNÇÕES ===
def iniciar_driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=opts)
    return driver

def get_preco(driver, url):
    try:
        driver.get(url)
        time.sleep(5)
        el = driver.find_element(By.CSS_SELECTOR, ".price__SalesPrice")
        preco_txt = el.text.strip().replace("R$", "").replace(",", ".")
        return float(preco_txt)
    except Exception as e:
        print("Erro ao ler preço:", e)
        return None

def enviar(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10,
        )
    except Exception as e:
        print("Erro Telegram:", e)

def verificar():
    driver = iniciar_driver()
    for p in PRODUTOS:
        preco = get_preco(driver, p["url"])
        if preco:
            print(f"{p['nome']}: R$ {preco:.2f}")
            if preco <= p["alvo"]:
                enviar(f"🔥 {p['nome']} baixou para R$ {preco:.2f}\n{p['url']}")
        else:
            print(f"❌ Não consegui ler o preço de {p['nome']}")
    driver.quit()

def keep_alive():
    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Bot ativo"
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    import threading
    threading.Thread(target=keep_alive).start()
    while True:
        verificar()
        print("Aguardando próxima checagem...\n")
        time.sleep(INTERVALO)

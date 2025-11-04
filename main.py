import streamlit as st
import requests
from bs4 import BeautifulSoup
from streamlit.components.v1 import html

st.set_page_config(layout="wide", page_title="Monitor de Preços")

# ---- Oculta cabeçalhos padrão ----
st.markdown("""
<style>
[data-testid="stHeader"] {visibility: hidden; height: 0%;}
.block-container {padding-top: 0rem;}
footer, #MainMenu {visibility: hidden;}
.card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 10px;
    display: flex;
    align-items: center;
    gap: 15px;
    box-shadow: 1px 1px 6px rgba(0,0,0,0.05);
    transition: all 0.2s ease-in-out;
}
.card:hover {
    transform: scale(1.01);
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
}
.card img {
    width: 120px;
    height: 120px;
    object-fit: contain;
    border-radius: 8px;
}
.card h4 {
    margin: 0;
    font-size: 1.1rem;
}
.card a {
    text-decoration: none;
    color: inherit;
}
</style>
""", unsafe_allow_html=True)

# ---- Lista de produtos ----
precos_e_links = [
    ("R$ 31,72", "https://www.centauro.com.br/bermuda-masculina-oxer-ls-basic-new-984889.html?cor=04"),
    ("R$ 53,99", "https://www.centauro.com.br/bermuda-masculina-oxer-mesh-mescla-983436.html?cor=MS"),
    ("R$ 31,49", "https://www.centauro.com.br/calcao-masculino-adams-liso-978059.html?cor=02"),
    ("R$ 1794", "https://shopee.com.br/Xiaomi-Poco-X7-Pro-512GB-256GB-12-Ram-5G-Vers%C3%A3o-Global-NFC-Original-Lacrado-e-Envio-Imediato-ADS-i.1351433975.20698075298"),
]

FATOR_ZOOM = 0.5
LARGURA_BASE_PIXELS = "150%"
ALTURA_BASE_PIXELS = 1000
BUFFER_ALTURA_STREAMLIT = 30
ALTURA_FINAL_STREAMLIT = int(ALTURA_BASE_PIXELS * FATOR_ZOOM) + BUFFER_ALTURA_STREAMLIT

st.markdown("<h6>🔎 Monitor de Preço</h6>", unsafe_allow_html=True)

# ---- Função para puxar preview da Shopee ----
def preview_shopee(url):
    """Retorna título, imagem e preço aproximado a partir da meta tag da Shopee."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.find("meta", property="og:title")
        image = soup.find("meta", property="og:image")
        price = soup.find("meta", property="product:price:amount")

        titulo = title["content"] if title else "Produto Shopee"
        imagem = image["content"] if image else "https://upload.wikimedia.org/wikipedia/commons/4/4f/Shopee_logo_2021.svg"
        preco_meta = price["content"] if price else "Ver preço no site"

        return titulo, imagem, preco_meta
    except Exception as e:
        return "Produto Shopee (visualização indisponível)", "https://upload.wikimedia.org/wikipedia/commons/4/4f/Shopee_logo_2021.svg", "Ver no site"

# ---- Loop principal ----
for i, (preco, link) in enumerate(precos_e_links):
    nome_produto = f"{i + 1})"

    st.markdown(f"""
    <div style="display: flex; align-items: baseline; gap: 15px; margin-bottom: -10px;">
        <h2 style="margin-bottom: 0;">{nome_produto}</h2>
        <p style="margin-bottom: 0; font-size: 1.2em; font-weight: bold; color: green;">{preco}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Shopee (usa preview) ---
    if "shopee.com.br" in link:
        titulo, imagem, preco_meta = preview_shopee(link)
        st.markdown(f"""
        <a href="{link}" target="_blank">
            <div class="card">
                <img src="{imagem}">
                <div>
                    <h4>{titulo}</h4>
                    <p><b>💰 {preco_meta}</b></p>
                    <p style="color:#888;font-size:0.9em;">Abrir na Shopee ↗️</p>
                </div>
            </div>
        </a>
        """, unsafe_allow_html=True)

    # --- Centauro (usa iframe normal) ---
    else:
        iframe = f"""
        <iframe src="{link}" width="{LARGURA_BASE_PIXELS}px" height="{ALTURA_BASE_PIXELS}px"
        style="border:1px solid #ddd; transform: scale({FATOR_ZOOM}); transform-origin: top left;"></iframe>
        """
        html(iframe, height=ALTURA_FINAL_STREAMLIT)

    st.markdown("---")

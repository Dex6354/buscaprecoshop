import streamlit as st
from streamlit.components.v1 import html
from urllib.parse import urlparse
import math

st.set_page_config(layout="wide", page_title="Monitor de Preços")

# --------------------------
# CSS Global
# --------------------------
st.markdown("""
<style>
[data-testid="stHeader"] { visibility: hidden; height: 0%; }
.block-container { padding-top: 0rem; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --------------------------
# Parâmetros
# --------------------------
FATOR_ZOOM = 0.4
LARGURA_BASE_PIXELS = "125%"
ALTURA_BASE_PIXELS = 800
BUFFER_ALTURA_STREAMLIT = 20
ALTURA_FINAL_STREAMLIT = int(ALTURA_BASE_PIXELS * FATOR_ZOOM) + BUFFER_ALTURA_STREAMLIT

# --------------------------
# Dados
# --------------------------
precos_e_links = [
    ("R$ 1600", "https://www.tudocelular.com/Poco/precos/n9834/Poco-X7-Pro.html"),
    ("R$ 31,18", "https://www.centauro.com.br/bermuda-masculina-oxer-ls-basic-new-984889.html?cor=02"),
    ("R$ 28,07", "https://www.centauro.com.br/bermuda-masculina-oxer-training-7-tecido-plano-981429.html?cor=02"),
    ("R$ 33,24", "https://www.centauro.com.br/bermuda-masculina-oxer-elastic-984818.html?cor=02"),
    ("R$ ", "https://www.centauro.com.br/conjunto-de-agasalho-masculino-asics-com-capuz-interlock-fechado-976758.html?cor=02"),
    ("R$ 1794", "https://shopee.com.br/Xiaomi-Poco-X7-Pro-512GB-256GB-12-Ram-5G-Vers%C3%A3o-Global-NFC-Original-Lacrado-e-Envio-Imediato-ADS-i.1351433975.20698075298"),
    ("👉R$ 2880 25,8kwh 399L", "https://www.consul.com.br/geladeira-consul-frost-free-duplex-com-freezer-embaixo-cre45mb/p"),
]

st.markdown("<h6>🔎 Monitor de Preço</h6>", unsafe_allow_html=True)

# --------------------------
# Função para estimar altura
# --------------------------
def estimate_text_block_height(html_text: str, base_width_px: int = 600) -> int:
    num_br = html_text.count("<br>")
    text_only = html_text.replace("<br>", " ").replace("&nbsp;", " ")
    approx_chars = len(text_only)
    est_lines = math.ceil(approx_chars / 40)
    total_lines = max(1, 1 + num_br, est_lines)
    return total_lines * 20 + 18

# --------------------------
# Loop de exibição
# --------------------------
for i, (preco_desejado, link_produto) in enumerate(precos_e_links):
    if not link_produto.strip():
        continue

    # Extrai domínio
    try:
        parsed = urlparse(link_produto)
        dominio = parsed.netloc.replace("www.", "") or "Ver produto"
    except:
        dominio = "Acessar produto"

    # Formata texto
    words = preco_desejado.split(" ")
    if len(words) >= 2 and (words[0] == "R$" or words[0] == "👉R$"):
        first_line = words[0] + " " + words[1]
        rest_lines = words[2:]
    else:
        first_line = words[0]
        rest_lines = words[1:]

    rest_lines = [w for w in rest_lines if w.strip()]
    texto_formatado = first_line + "<br>" + "<br>".join(rest_lines) if rest_lines else first_line

    nome_produto = f"{i + 1}"

    # -------------------------------
    # BLOCO HTML (com domínio embaixo)
    # -------------------------------
    bloco_html = f"""
    <div style="margin-bottom: 4px; font-family: Arial, Helvetica, sans-serif;">

        <h3 style="margin:0 0 6px 0; font-size:16px;">
            {nome_produto})
        </h3>

        <p style="margin:0; font-size: 18px; font-weight: 700; color: green; line-height:1.3;">
            {texto_formatado}
        </p>

        <!-- Domínio como hiperlink -->
        <p style="margin:6px 0 0 0; font-size: 13px; color:#333;">
            🔗 <a href="{link_produto}" target="_blank" rel="noopener noreferrer">
                {dominio}
            </a>
        </p>

    </div>
    """

    bloco_height = max(60, estimate_text_block_height(texto_formatado))
    html(bloco_html, height=bloco_height)

    # -------------------------------
    # IFRAME DO PRODUTO
    # -------------------------------
    iframe_html = f"""
    <iframe
        src="{link_produto}"
        width="{LARGURA_BASE_PIXELS}"
        height="{ALTURA_BASE_PIXELS}px"
        style="
            border: 1px solid #ddd;
            border-radius: 8px;
            transform: scale({FATOR_ZOOM});
            transform-origin: top left;
            display: block;
        ">
    </iframe>
    """

    html(iframe_html, height=ALTURA_FINAL_STREAMLIT + 8)
    st.divider()

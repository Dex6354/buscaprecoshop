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
    # ... (adicione o restante se quiser)
]

st.markdown("<h6>🔎 Monitor de Preço</h6>", unsafe_allow_html=True)

# --------------------------
# Função utilitária para estimar altura (em px) do bloco de texto
# --------------------------
def estimate_text_block_height(html_text: str, base_width_px: int = 600) -> int:
    """
    Estima a altura necessária para um bloco HTML simples contendo algumas <br>.
    Não é perfeito, mas é conservador o suficiente para evitar sobreposição.
    """
    # Conta quebras de linha explícitas <br>
    num_br = html_text.count("<br>")
    # Conta comprimento aproximado sem tags
    text_only = html_text.replace("<br>", " ").replace("&nbsp;", " ")
    approx_chars = len(text_only)
    # Estima número de "linhas" por largura
    avg_chars_per_line = 40  # chute conservador (a depender do tamanho da fonte)
    est_lines_from_chars = math.ceil(approx_chars / avg_chars_per_line)
    total_lines = max(1, 1 + num_br, est_lines_from_chars)
    # Altura por linha (px) - conservador
    height_per_line = 20
    padding = 18  # top+bottom padding
    return total_lines * height_per_line + padding

# --------------------------
# Loop de exibição
# --------------------------
for i, (preco_desejado, link_produto) in enumerate(precos_e_links):
    if not link_produto.strip():
        continue

    # Extrai domínio
    try:
        parsed = urlparse(link_produto)
        texto_link = parsed.netloc.replace("www.", "") or "Ver Link"
    except:
        texto_link = "Acessar Produto"

    # Monta texto formatado (com <br> para quebras explícitas)
    words = preco_desejado.split(" ")
    if len(words) >= 2 and (words[0] == "R$" or words[0] == "👉R$"):
        first_line = words[0] + " " + words[1]
        rest_lines = words[2:]
    else:
        first_line = words[0] if words else ""
        rest_lines = words[1:] if len(words) > 1 else []
    rest_lines = [w for w in rest_lines if w.strip()]
    if rest_lines:
        texto_formatado = first_line + "<br>" + "<br>".join(rest_lines)
    else:
        texto_formatado = first_line

    nome_produto = f"{i + 1}"

    # --- bloco HTML (renderizado via st.components.v1.html com altura estimada)
    bloco_html = f"""
    <div style="margin-bottom: 4px; font-family: Arial, Helvetica, sans-serif;">
        <h3 style="margin:0 0 6px 0; font-size:16px;">{nome_produto})</h3>
        <p style="margin:0; font-size: 18px; font-weight: 700; color: green; line-height:1.3;">
            {texto_formatado}
        </p>
        <p style="margin:6px 0 0 0; font-size: 13px; color: #333;">
            <a href="{link_produto}" target="_blank" rel="noopener noreferrer">{texto_link}</a>
        </p>
    </div>
    """

    # Estima altura do bloco de texto e renderiza (altura dinamica evita corte/sobreposição)
    bloco_height = estimate_text_block_height(texto_formatado)
    # adiciona um mínimo seguro
    bloco_height = max(60, bloco_height)
    html(bloco_html, height=bloco_height)

    # --- iframe (componente separado; sempre renderizado depois do bloco de texto)
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
    # Altura do html() que contém o iframe deve considerar o scale e um pequeno espaçamento
    html(iframe_html, height=ALTURA_FINAL_STREAMLIT + 8)

    st.divider()

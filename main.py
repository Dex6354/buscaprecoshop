import streamlit as st
from streamlit.components.v1 import html
from urllib.parse import urlparse

st.set_page_config(
    layout="wide",
    page_title="Monitor de Preços"
)

# --------------------------
# 1. CSS Global
# --------------------------
st.markdown("""
<style>
[data-testid="stHeader"] {
    visibility: hidden;
    height: 0%;
}
.block-container { padding-top: 0rem; }
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --------------------------
# 2. Parâmetros Visuais
# --------------------------
FATOR_ZOOM = 0.4
LARGURA_BASE_PIXELS = "125%"
ALTURA_BASE_PIXELS = 800
BUFFER_ALTURA_STREAMLIT = 20
ALTURA_FINAL_STREAMLIT = int(ALTURA_BASE_PIXELS * FATOR_ZOOM) + BUFFER_ALTURA_STREAMLIT

# --------------------------
# 3. Lista de preços
# --------------------------
precos_e_links = [
    ("R$ 1600", "https://www.tudocelular.com/Poco/precos/n9834/Poco-X7-Pro.html"),
    ("R$ 31,18", "https://www.centauro.com.br/bermuda-masculina-oxer-ls-basic-new-984889.html?cor=02"),
    ("R$ 28,07", "https://www.centauro.com.br/bermuda-masculina-oxer-training-7-tecido-plano-981429.html?cor=02"),
    ("R$ 33,24", "https://www.centauro.com.br/bermuda-masculina-oxer-elastic-984818.html?cor=02"),
]

# --------------------------
# 4. Título
# --------------------------
st.markdown("<h6>🔎 Monitor de Preço</h6>", unsafe_allow_html=True)

# --------------------------
# 5. Loop dos produtos
# --------------------------
for i, (preco_desejado, link_produto) in enumerate(precos_e_links):

    if not link_produto.strip():
        continue

    # Extrai domínio
    try:
        parsed_url = urlparse(link_produto)
        texto_link = parsed_url.netloc.replace("www.", "")
        if not texto_link:
            texto_link = "Ver Link"
    except:
        texto_link = "Acessar Produto"

    # Quebra o preço em linhas
    words = preco_desejado.split(" ")

    if len(words) >= 2 and (words[0] == "R$" or words[0] == "👉R$"):
        first_line = words[0] + " " + words[1]
        rest_lines = words[2:]
    else:
        first_line = words[0] if words else ""
        rest_lines = words[1:] if len(words) > 1 else []

    rest_lines = [line for line in rest_lines if line.strip()]

    if rest_lines:
        texto_formatado = first_line + "<br>" + "<br>".join(rest_lines)
    else:
        texto_formatado = first_line

    nome_produto = f"{i + 1}"

    # --------------------------
    # EXIBE O BLOCO DE TEXTO NORMALMENTE (sem iframe junto)
    # --------------------------
    st.markdown(f"""
    <div style="margin-bottom: 10px;">
        <h3 style="margin-bottom: 4px;">{nome_produto})</h3>

        <p style="margin: 0; font-size: 1.1em; font-weight: bold; color: green; line-height: 1.4;">
            {texto_formatado}
        </p>

        <p style="margin: 2px 0 10px 0; font-size: 0.8em;">
            <a href="{link_produto}" target="_blank">{texto_link}</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------
    # AGORA EXIBE O IFRAME SEPARADO (nunca sobrepõe)
    # --------------------------
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
        ">
    </iframe>
    """

    html(iframe_html, height=ALTURA_FINAL_STREAMLIT)

    st.divider()

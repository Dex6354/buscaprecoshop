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
    ("R$ 100", "https://www.centauro.com.br/conjunto-de-agasalho-oxer-replayer-981478.html?cor=02"),
    ("R$ 103,98", "https://www.centauro.com.br/conjunto-de-agasalho-oxer-replayer-981478.html?cor=05"),
    ("R$ 28,49", "https://www.centauro.com.br/camiseta-masculina-oxer-manga-curta-regulacao-termica-987888.html?cor=02"),
    ("R$ 38", "https://www.centauro.com.br/camiseta-masculina-oxer-manga-curta-tunin-988506.html?cor=02"),
    ("R$ ", "https://www.centauro.com.br/conjuto-de-agasalho-masculino-asics-interlock-bolso-fusionado-976753.html?cor=02"),
    ("R$ ", "https://www.centauro.com.br/conjunto-de-agasalho-masculino-asics-com-capuz-interlock-fechado-976758.html?cor=02"),
    ("R$ 1794", "https://shopee.com.br/Xiaomi-Poco-X7-Pro-512GB-256GB-12-Ram-5G-Vers%C3%A3o-Global-NFC-Original-Lacrado-e-Envio-Imediato-ADS-i.1351433975.20698075298"),
("👉R$ 2880 25,8kwh 399L", "https://www.consul.com.br/geladeira-consul-frost-free-duplex-com-freezer-embaixo-cre45mb/p"),
("👉R$ 2.659,05 39,7kwh 390L", "https://www.buscape.com.br/geladeira/geladeira-electrolux-efficient-if43-frost-free-duplex-390-litros?_lc=88&searchterm=Geladeira%20Electrolux%20Frost%20Free%20320L%20Duplex%20Branca"),
("👉R$ 2417,07 24,9kwh CRM44MB 377L", "https://www.compracerta.com.br/geladeira-frost-free-duplex-consul---crm44mb-20124213/p"),
("👉R$ 2570 24,9kwh 377L", "https://www.consul.com.br/geladeira-frost-free-duplex-consul-crm44mb/p?idsku=326183363&skuId=326183363&utm_campaign=comparador_mpi_d2c&utm_medium=comparadores&utm_source=zoom&utm_term=c2145529c657414290fbf27d974defa5&utmi_campaign=pla&utmi_cp=pla"),
("R$2599 43,6kwh 310L", "https://loja.electrolux.com.br/geladeira-refrigerador-frost-free-310-litros-branco-tf39-electrolux/p?idsku=2003557"),
("R$2469,05 46,8kwh 320L", "https://www.webcontinental.com.br/geladeira-electrolux-frost-free-320l-duplex-branca-tf38-220v-001006002311/p?utm_medium=cpc&utm_source=zoom&utm_campaign=6c392c85896542cdae9f0d0264ab5271"),
("R$ 2999 35,3kwh 431L", "https://loja.electrolux.com.br/geladeira-electrolux-frost-free-431l-efficient-autosense-duplex-branca--tf70-/p?idsku=310127216&skuId=310127216"),
("R$ 2744,64 48,8kwh 375L", "https://www.brastemp.com.br/geladeira-brastemp-frost-free-duplex-375-litros-cor-branca-com-espaco-adapt-brm45jb/p?idsku=326031047&utm_source=google&utm_medium=organic&utm_campaign=shopping"),
("R$ 2790 26,9kwh 455L", "https://www.consul.com.br/geladeira-frost-free-duplex-branca-consul-crm56mb/p"),
("R$ 2689 35,5kwh 391L", "https://www.buscape.com.br/geladeira/geladeira-samsung-evolution-rt38dg6120s9fz-frost-free-duplex-391-litros-cor-inox?_lc=88&searchterm=Geladeira%20"),
("R$ 2500 54kwh 375L 76x210 74x188x70", "https://clube.magazineluiza.com.br/nubankcashback/geladeira-brastemp-frost-free-duplex-375l-branca-com-com-compartimento-extrafrio-fresh-zone-brm44hb/p/013085501/ED/REF2"),
("R$ ", ""),
]

st.markdown("<h6>🔎 Monitor de Preço</h6>", unsafe_allow_html=True)

# --------------------------
# Função utilitária para estimar altura (em px) do bloco de texto
# --------------------------
def estimate_text_block_height(html_text: str, base_width_px: int = 600) -> int:
    """
    Estima a altura necessária para um bloco HTML.
    Ajustado para contar explicitamente todas as linhas de texto,
    incluindo quebras de linha explícitas e quebras por largura de texto.
    """
    # Alturas aproximadas (pixels) para cada elemento visual:
    HEIGHT_TITLE = 25    # Altura do h3 (nome do produto) + margin
    HEIGHT_PRICE_LINE = 25 # Altura da linha de preço (font-size: 18px + line-height)
    HEIGHT_LINK_LINE = 20  # Altura da linha do link (font-size: 13px + margin)
    PADDING_EXTRA = 15     # Padding extra de segurança

    # 1. Conta quebras de linha explícitas <br> no preço/descrição
    num_br = html_text.count("<br>")
    
    # 2. Estima quebras de linha por largura (para a primeira linha do preço/descrição)
    text_only = html_text.replace("<br>", " ").replace("&nbsp;", " ")
    
    # A primeira linha (preço) não deve quebrar, mas vamos usar como base para a contagem de palavras
    
    # Calcula o número total de linhas de preço/descrição (1 linha base + num_br)
    # Ex: "R$ 2880<br>25,8kwh<br>399L" tem 3 linhas (1 + 2 <br>)
    total_text_lines = 1 + num_br
    
    # 3. Calcula a altura total necessária:
    total_height = (
        HEIGHT_TITLE +              # Altura do Título (Ex: "1)")
        (total_text_lines * HEIGHT_PRICE_LINE) + # Altura das linhas de Preço/Descrição
        HEIGHT_LINK_LINE +          # Altura do Link/Domínio
        PADDING_EXTRA               # Buffer
    )
    
    return total_height

# --------------------------
# Loop de exibição
# --------------------------
for i, (preco_desejado, link_produto) in enumerate(precos_e_links):
    if not link_produto.strip():
        continue

    # Extrai domínio para o texto do link
    try:
        parsed = urlparse(link_produto)
        # Remove 'www.' para exibir apenas o domínio principal
        texto_link = parsed.netloc.replace("www.", "") or "Ver Link" 
    except:
        texto_link = "Acessar Produto"

    # Monta texto formatado (com <br> para quebras explícitas)
    words = preco_desejado.split(" ")
    
    # Lógica para separar a primeira linha do preço/sinalizador das demais informações
    if len(words) >= 2 and (words[0] == "R$" or words[0] == "👉R$"):
        # Se começar com R$ ou 👉R$, junta os dois primeiros elementos
        first_line = words[0] + " " + words[1]
        rest_lines = words[2:]
    else:
        # Caso contrário, o primeiro elemento é a primeira linha
        first_line = words[0] if words else ""
        rest_lines = words[1:] if len(words) > 1 else []
        
    rest_lines = [w for w in rest_lines if w.strip()]
    if rest_lines:
        # Adiciona quebras de linha entre as palavras restantes
        texto_formatado = first_line + "<br>" + "<br>".join(rest_lines)
    else:
        texto_formatado = first_line

    nome_produto = f"{i + 1}"

    # --- bloco HTML (renderizado via st.components.v1.html com altura estimada)
    # Garante que o texto e o link sejam renderizados antes do iframe
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

    # Estima altura do bloco de texto e renderiza
    bloco_height = estimate_text_block_height(texto_formatado)
    bloco_height = max(85, bloco_height) # Garante um mínimo seguro
    html(bloco_html, height=bloco_height)

    # --- iframe (componente separado; sempre renderizado DEPOIS do bloco de texto)
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

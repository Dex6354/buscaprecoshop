import streamlit as st
from streamlit.components.v1 import html
from urllib.parse import urlparse

st.set_page_config(
    layout="wide", 
    page_title="Monitor de Preços"
)

## 1. Configurações e Estilos (CSS)
st.markdown(
    """
    <style>
    /* Oculta o cabeçalho padrão do Streamlit */
    [data-testid="stHeader"] {
        visibility: hidden;
        height: 0%;
    }
    /* Reduz o padding superior do conteúdo */
    .block-container { 
        padding-top: 0rem; 
    }
    /* Oculta o footer e o menu principal */
    footer {
        visibility: hidden;
    }
    #MainMenu {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

---

## 2. Parâmetros de Exibição
# --- PARÂMETROS DE TAMANHO AJUSTADOS ---

FATOR_ZOOM = 0.4
# Usa 100vw (100% da largura da viewport) para melhor responsividade
LARGURA_BASE_PIXELS = "100vw" 
ALTURA_BASE_PIXELS = 800  
BUFFER_ALTURA_STREAMLIT = 20 
# Calcula a altura final para o componente Streamlit
ALTURA_FINAL_STREAMLIT = int(ALTURA_BASE_PIXELS * FATOR_ZOOM) + BUFFER_ALTURA_STREAMLIT

# --- FIM DOS PARÂMETROS ---

## 3. Dados de Preço e Link
precos_e_links = [
    ("R$ 1600", "https://www.tudocelular.com/Poco/precos/n9834/Poco-X7-Pro.html"),
    ("R$ 31,18", "https://www.centauro.com.br/bermuda-masculina-oxer-ls-basic-new-984889.html?cor=02"),
    ("R$ 28,07", "https://www.centauro.com.br/bermuda-masculina-oxer-training-7-tecido-plano-981429.html?cor=02"),
    ("R$ 33,24", "https://www.centauro.com.br/bermuda-masculina-oxer-elastic-984818.html?cor=02"),
    ("R$ 100", "https://www.centauro.com.br/conjunto-de-agasalho-oxer-replayer-981478.html?cor=02"),
    ("R$ 103,98", "https://www.centauro.com.br/conjunto-de-agasalho-oxer-replayer-981478.html?cor=05"),
    ("R$ 28,49", "https://www.centauro.com.br/camiseta-masculina-oxer-manga-curta-regulacao-termica-987888.html?cor=02"),
    ("R$ 38", "https://www.centauro.com.br/camiseta-masculina-oxer-manga-curta-tunin-988506.html?cor=02"),
    # Itens sem preço ou link para teste (serão ignorados)
    ("R$ ", "https://www.centauro.com.br/conjuto-de-agasalho-masculino-asics-interlock-bolso-fusionado-976753.html?cor=02"),
    ("R$ ", "https://www.centauro.com.br/conjunto-de-agasalho-masculino-asics-com-capuz-interlock-fechado-976758.html?cor=02"),
    ("R$ 1794", "https://shopee.com.br/Xiaomi-Poco-X7-Pro-512GB-256GB-12-Ram-5G-Vers%C3%A3o-Global-NFC-Original-Lacrado-e-Envio-Imediato-ADS-i.1351433975.20698075298"),
    ("👉R$ 2880 25,8kwh 39L", "https://www.consul.com.br/geladeira-consul-frost-free-duplex-com-freezer-embaixo-cre45mb/p"),
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
    ("R$ ", ""), # Item vazio (será ignorado)
]

---

## 4. Renderização dos Itens

st.markdown("<h6>🔎 Monitor de Preço</h6>", unsafe_allow_html=True)

for i, (preco_desejado, link_produto) in enumerate(precos_e_links):
    
    if not link_produto.strip():
        continue
    
    # --- 4.1 LÓGICA DE FORMATAÇÃO DO TEXTO ---
    
    # 1. Cria o texto amigável para o link (netloc)
    try:
        parsed_url = urlparse(link_produto)
        texto_link = parsed_url.netloc 
        if texto_link.startswith("www."):
            texto_link = texto_link[4:]
        if not texto_link:
            texto_link = "Ver Link"
    except Exception:
        texto_link = "Acessar Produto"

    # 2. Formata o preço (primeira palavra em uma linha, resto em outras)
    words = preco_desejado.split(' ')
    
    if len(words) > 1 and (words[0] == 'R$' or words[0] == '👉R$'):
        first_line = words[0] + " " + words[1]
        rest_lines = words[2:]
    else:
        first_line = words[0]
        rest_lines = words[1:]
    
    # Adiciona <br> para quebrar as linhas das informações extras
    rest_lines_filtered = [line for line in rest_lines if line.strip()]
    if rest_lines_filtered:
        texto_formatado = first_line + "<br>" + "<br>".join(rest_lines_filtered)
    else:
        texto_formatado = first_line
        
    nome_produto = f"{i + 1}"
    
    # --- 4.2 RENDERIZAÇÃO DO PREÇO/LINK (st.markdown) ---
    st.markdown(f"""
    <div style="margin-bottom: -15px;">
        <h3 style="margin-bottom: 5px;">{nome_produto})</h3>
        
        <p style="margin-bottom: 5px; font-size: 1.1em; font-weight: bold; color: green; line-height: 1.4;">
            {texto_formatado} 
        </p>
        
        <p style="margin-bottom: 5px; font-size: 0.8em; max-width: 600px; overflow-wrap: break-word;">
            <a href="{link_produto}" target="_blank">{texto_link}</a> 
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- 4.3 RENDERIZAÇÃO DO IFRAME (st.components.v1.html) ---
    html_content = f"""
    <iframe 
        src="{link_produto}" 
        width="{LARGURA_BASE_PIXELS}" 
        height="{ALTURA_BASE_PIXELS}px"
        style="
            border: 1px solid #ddd;
            border-radius: 8px;
            /* Aplica o zoom e ajusta a origem para o canto superior esquerdo */
            transform: scale({FATOR_ZOOM}); 
            transform-origin: top left;
            margin-top: 5px; 
        " 
    ></iframe>
    """

    # O componente HTML é injetado com a altura final calculada
    st.components.v1.html(html_content, height=ALTURA_FINAL_STREAMLIT)
    
    st.markdown("---")

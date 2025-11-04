import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    layout="wide", 
    page_title="Monitor de Preços"
)

st.markdown(
    """
    <style>
    [data-testid="stHeader"] {
            visibility: hidden;
            height: 0%;
        }
        .block-container { padding-top: 0rem; }
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

FATOR_ZOOM = 0.5

LARGURA_BASE_PIXELS = "150%" # Tamanho base para o conteúdo caber
ALTURA_BASE_PIXELS = 1000  # Tamanho base para o conteúdo caber

BUFFER_ALTURA_STREAMLIT = 30 # Espaço extra para a rolagem do componente

# Calcula a altura final do componente Streamlit (altura base escalada + buffer)
ALTURA_FINAL_STREAMLIT = int(ALTURA_BASE_PIXELS * FATOR_ZOOM) + BUFFER_ALTURA_STREAMLIT

# --- ESTRUTURA DE DADOS UTILIZADA (LISTA DE TUPLAS) ---
# A tupla é: (Preço, Link)
precos_e_links = [
    ("R$ 31,72", "https://www.centauro.com.br/bermuda-masculina-oxer-ls-basic-new-984889.html?cor=04"),
    ("R$ 53,99", "https://www.centauro.com.br/bermuda-masculina-oxer-mesh-mescla-983436.html?cor=MS"),
    ("R$ 31,49", "https://www.centauro.com.br/calcao-masculino-adams-liso-978059.html?cor=02"),
    ("R$ 1794", "https://shopee.com.br/Xiaomi-Poco-X7-Pro-512GB-256GB-12-Ram-5G-Vers%C3%A3o-Global-NFC-Original-Lacrado-e-Envio-Imediato-ADS-i.1351433975.20698075298"),
]
# --- FIM DA ESTRUTURA ---

# Título principal diminuído (usando h2 em vez de h1)
st.markdown("<h6>🔎 Monitor de Preço</h6>", unsafe_allow_html=True)

# Iteramos sobre a lista de tuplas: (Preço, Link)
for i, (preco_desejado, link_produto) in enumerate(precos_e_links):
    
    link_final_iframe = link_produto
    exibir_iframe = True
    
    # --- TRATAMENTO PARA SHOPEE (E OUTROS QUE FORÇAM O APP) ---
    if "shopee.com.br" in link_produto:
        
        # 1. Tenta anexar o parâmetro de desativação de app
        if '?' in link_produto:
            # Se já tem '?', anexa com '&'
            link_final_iframe = link_produto + "&is_from_app=false"
        else:
            # Se não tem, anexa com '?'
            link_final_iframe = link_produto + "?is_from_app=false"

        # 2. Estratégia de fallback: Ignorar o iframe, pois ele falha
        # Se você tentou o parâmetro e ainda falha (o que parece ser o caso), 
        # avisamos o usuário e mostramos o link direto no título, pulando o iframe.
        exibir_iframe = False 
    
    nome_produto = f"{i + 1}" # Número de ordem
    
    # Exibição: O preço (primeiro elemento da tupla) é exibido em destaque e o link é oculto no texto "Acessar Produto"
    st.markdown(f"""
    <div style="display: flex; align-items: baseline; gap: 15px; margin-bottom: -10px;">
        <h2 style="margin-bottom: 0;">{nome_produto})</h2>
        <p style="margin-bottom: 0; font-size: 1.2em; font-weight: bold; color: green;">
            {preco_desejado}  </p>
        <p style="margin-bottom: 0; font-size: 0.8em; max-width: 600px; overflow-wrap: break-word;">
            <a href="{link_produto}" target="_blank">Acessar Produto</a> </p>
    </div>
    """, unsafe_allow_html=True)
    
    if exibir_iframe:
        # Apenas carrega o iframe se não for Shopee (ou se o parâmetro funcionar)
        html_content = f"""
        <iframe 
            src="{link_final_iframe}" 
            width="{LARGURA_BASE_PIXELS}px" 
            height="{ALTURA_BASE_PIXELS}px"
            style="
                border: 1px solid #ddd; /* Borda mais suave */
                transform: scale({FATOR_ZOOM}); 
                transform-origin: top left;
                margin-top: 5px; 
            " 
        ></iframe>
        """
        # Exibe o componente HTML/iFrame
        st.components.v1.html(html_content, height=ALTURA_FINAL_STREAMLIT)
    else:
        # Mensagem para o usuário sobre a impossibilidade de embutir
        st.warning(f"🛑 O link da **Shopee** (Produto {nome_produto}) está sendo forçado para o app. Use o link **'Acessar Produto'** acima para ver no navegador.")

    
    # SEPARADOR VISUAL entre os produtos
    st.markdown("---")

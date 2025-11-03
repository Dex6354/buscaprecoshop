import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    layout="wide", 
    page_title="Monitor de Preços - Embed Centauro"
)

# --- Configurações de Tamanho e Zoom ---
# O FATOR_ZOOM controla o quão pequeno o conteúdo aparecerá (0.4 = 40% do tamanho original)
FATOR_ZOOM = 0.4 

# Definimos a LARGURA/ALTURA BASE que o iframe renderizará ANTES do scale.
# Escolha um valor grande o suficiente para o conteúdo caber.
LARGURA_BASE_PIXELS = "100%" # Tamanho base para o conteúdo caber
ALTURA_BASE_PIXELS = 1000  # Tamanho base para o conteúdo caber

BUFFER_ALTURA_STREAMLIT = 30 # Espaço extra para a rolagem do componente

# Calcula a altura final do componente Streamlit (altura base escalada + buffer)
ALTURA_FINAL_STREAMLIT = int(ALTURA_BASE_PIXELS * FATOR_ZOOM) + BUFFER_ALTURA_STREAMLIT

# A largura final visível será a Largura Base * FATOR_ZOOM.
# Para que ele ocupe mais espaço na tela, você pode aumentar LARGURA_BASE_PIXELS.
# **A variável LARGURA_IFRAME_EMBED não é mais necessária nesta abordagem com scale.**

# --- Fim das Configurações ---


lista_de_urls = [
    "https://www.centauro.com.br/bermuda-masculina-oxer-ls-basic-new-984889.html?cor=04",
    "https://www.centauro.com.br/bermuda-masculina-oxer-mesh-mescla-983436.html?cor=MS",
]

st.title("Monitor de Preços")

# Usamos enumerate para obter o índice (i) e a URL (link_produto)
for i, link_produto in enumerate(lista_de_urls):
    
    nome_produto = f"Produto Monitorado #{i + 1}" 
    
    st.header(nome_produto)
    
    # Exibe o link original
    st.markdown(f"**Link Original:** [{link_produto}]({link_produto})", unsafe_allow_html=True)

    # --- AJUSTES COM CSS TRANSFORM: SCALE ---
    
    # O style define:
    # 1. Um tamanho base grande (LARGURA_BASE_PIXELS/ALTURA_BASE_PIXELS).
    # 2. transform: scale(FATOR_ZOOM) para diminuir a exibição.
    # 3. transform-origin: top left; garante que o "zoom" parta do canto superior esquerdo.
    
    html_content = f"""
    <iframe 
        src="{link_produto}" 
        width="{LARGURA_BASE_PIXELS}px" 
        height="{ALTURA_BASE_PIXELS}px"
        style="
            border: 1px solid #ccc; /* Para visualização */
            transform: scale({FATOR_ZOOM}); 
            transform-origin: top left;
            margin-top: 20px;
        " 
    ></iframe>
    """

    # Exibe o componente HTML/iFrame
    # IMPORTANTE: A altura (height) do st.components.v1.html deve refletir o TAMANHO FINAL ESCALADO
    st.components.v1.html(html_content, height=ALTURA_FINAL_STREAMLIT)
    
    # SEPARADOR VISUAL entre os produtos
    st.markdown("---")

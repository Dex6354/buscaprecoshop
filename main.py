import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    layout="wide", 
    page_title="Monitor de Preços - Embed Centauro"
)

# --- Configurações de Tamanho e Zoom ---
ALTURA_IFRAME = 500  # Altura base do viewport do iframe em pixels
LARGURA_IFRAME_EMBED = "80%" # Usar um valor fixo ou '100%' da coluna, mas 'scale' funciona melhor com base fixa
BUFFER_ALTURA_STREAMLIT = 30 

# NOVO: Fator de escala para simular o zoom. 
# 1.0 = 100% (tamanho normal)
# 0.8 = 80% (conteúdo parece 20% menor)
FATOR_ZOOM = 0.4

# Calcula a largura e altura ajustadas para o 'scale'
# O navegador renderiza o iframe no tamanho base (ex: 800px) e depois o escala.
LARGURA_AJUSTADA = "800px" # Tamanho base maior que o desejado para compensar a escala
ALTURA_AJUSTADA = "800px" # Tamanho base maior que o desejado para compensar a escala

# O height final do componente Streamlit deve ser a altura base escalada, mais o buffer
ALTURA_FINAL_STREAMLIT = int(int(ALTURA_AJUSTADA.replace("px", "")) * FATOR_ZOOM) + BUFFER_ALTURA_STREAMLIT
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
    # 1. Um tamanho base grande (800px) para o conteúdo caber.
    # 2. transform: scale(FATOR_ZOOM) para diminuir a exibição.
    # 3. transform-origin: top left; garante que o "zoom" parta do canto superior esquerdo.
    
    html_content = f"""
    <iframe 
        src="{link_produto}" 
        width="{LARGURA_AJUSTADA}" 
        height="{ALTURA_AJUSTADA}"
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

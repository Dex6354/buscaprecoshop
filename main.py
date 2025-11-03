import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    layout="wide", 
    page_title="Monitor de Preços - Embed Centauro"
)

# Dimensões para a visualização (ajuste conforme necessário)
ALTURA_IFRAME = 500
# NOVO: Reduzimos para 80% para dar mais espaço livre à direita
LARGURA_IFRAME_EMBED = "80%" 
BUFFER_ALTURA_STREAMLIT = 30 

# Lista contendo APENAS as URLs dos produtos que você deseja monitorar.
lista_de_urls = [
    "https://www.centauro.com.br/bermuda-masculina-oxer-ls-basic-new-984889.html?cor=04",
    "https://www.centauro.com.br/bermuda-masculina-oxer-mesh-mescla-983436.html?cor=MS",
]

st.title("Monitor de Preços")

# Usamos enumerate para obter o índice (i) e a URL (link_produto)
for i, link_produto in enumerate(lista_de_urls):
    
    nome_produto = f"Produto Monitorado #{i + 1}" 
    
    st.header(nome_produto)
    
    st.markdown(f"**Link Original:** [{link_produto}]({link_produto})", unsafe_allow_html=True)

    # O conteúdo do iframe ainda carregará no topo de sua caixa (devido a restrições de segurança/navegador)
    # O style="margin-top: 20px;" move a CAIXA inteira 20px para baixo.
    
    html_content = f"""
    <iframe 
        src="{link_produto}" 
        width="{LARGURA_IFRAME_EMBED}" 
        height="{ALTURA_IFRAME}px"
        style="margin-top: 20px;" 
    ></iframe>
    """

    st.components.v1.html(html_content, height=ALTURA_IFRAME + BUFFER_ALTURA_STREAMLIT)
    
    st.markdown("---")

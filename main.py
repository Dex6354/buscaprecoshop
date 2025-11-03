import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    layout="wide", 
    page_title="Monitor de Preços - Embed Centauro"
)

# Dimensões para a visualização (ajuste conforme necessário)
ALTURA_IFRAME = 500  # Altura em pixels para a visualização
# NOVO: Reduzimos a largura do iframe para deixar espaço à direita.
# Exemplo: 90% da largura da coluna (que já é o máximo no layout 'wide')
LARGURA_IFRAME_EMBED = "90%" 
# Ajuste para deixar o espaço de rolagem vazio à direita
BUFFER_ALTURA_STREAMLIT = 30 # Buffer para acomodar títulos/espaçamento no Streamlit

# Lista contendo APENAS as URLs dos produtos que você deseja monitorar.
lista_de_urls = [
    "https://www.centauro.com.br/bermuda-masculina-oxer-ls-basic-new-984889.html?cor=04",
    "https://www.centauro.com.br/bermuda-masculina-oxer-mesh-mescla-983436.html?cor=MS",
]

st.title("Monitor de Preços")

# Usamos enumerate para obter o índice (i) e a URL (link_produto)
for i, link_produto in enumerate(lista_de_urls):
    
    # Define um título baseado no índice (Ex: Produto 1, Produto 2, etc.)
    nome_produto = f"Produto Monitorado #{i + 1}" 
    
    st.header(nome_produto)
    
    # Exibe o link original
    st.markdown(f"**Link Original:** [{link_produto}]({link_produto})", unsafe_allow_html=True)

    # --- AJUSTES AQUI ---
    
    # 1. Deslocamento vertical de 20px (usando style="margin-top: 20px;")
    # 2. Largura reduzida (usando a nova LARGURA_IFRAME_EMBED)
    
    html_content = f"""
    <iframe 
        src="{link_produto}" 
        width="{LARGURA_IFRAME_EMBED}" 
        height="{ALTURA_IFRAME}px"
        style="margin-top: 20px;" 
    ></iframe>
    """

    # Exibe o componente HTML/iFrame
    # Manter a altura total para garantir que o conteúdo de baixo não seja cortado.
    st.components.v1.html(html_content, height=ALTURA_IFRAME + BUFFER_ALTURA_STREAMLIT)
    
    # SEPARADOR VISUAL entre os produtos
    st.markdown("---")

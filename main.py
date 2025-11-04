import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    layout="wide", 
    page_title="Monitor de Preços - Embed Centauro"
)

# 1. CONFIGURAÇÃO DE ESTILO AVANÇADA: Oculta o cabeçalho e fixa o título no topo
st.markdown(
    """
    <style>
        /* Oculta o cabeçalho padrão do Streamlit */
        [data-testid="stHeader"] {
            visibility: hidden;
            height: 0%;
        }
        
        /* Remove o padding superior do corpo da aplicação Streamlit */
        .stApp {
            padding-top: 0px !important; 
        }
        
        /* ESTILO DO TÍTULO FIXO */
        #titulo-topo {
            position: fixed; /* Garante que o título fique fixo no topo da janela */
            top: 0;
            left: 0;
            width: 100%;
            background-color: white; /* Adiciona um fundo para garantir que não fique por baixo de outros elementos */
            padding: 10px 20px;
            z-index: 1000; /* Garante que fique acima de outros conteúdos */
            box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* Opcional: Sombra sutil */
            margin: 0; /* Remove margem padrão */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. INSERÇÃO DO TÍTULO FIXO NO TOPO
# Este H3 agora está configurado com position: fixed no CSS acima
st.markdown('<h3 id="titulo-topo">Monitor de Preços</h3>', unsafe_allow_html=True)

FATOR_ZOOM = 0.5

LARGURA_BASE_PIXELS = "150%" 
ALTURA_BASE_PIXELS = 1000

BUFFER_ALTURA_STREAMLIT = 30 

ALTURA_FINAL_STREAMLIT = int(ALTURA_BASE_PIXELS * FATOR_ZOOM) + BUFFER_ALTURA_STREAMLIT

lista_de_urls = [
    "https://www.centauro.com.br/bermuda-masculina-oxer-ls-basic-new-984889.html?cor=04",
    "https://www.centauro.com.br/bermuda-masculina-oxer-mesh-mescla-983436.html?cor=MS",
]

# Como o título agora está fixo (position: fixed), precisamos adicionar um espaçamento
# no conteúdo principal (abaixo dele) para que o conteúdo não fique por baixo do título fixo.
PADDING_DO_TITULO_FIXO = 60 # Deve ser maior que a altura do seu título fixo (que agora tem padding de 10px + altura do h3)

# 3. CONTEÚDO PRINCIPAL (COM PAD INICIAL)
# Aplica o padding superior para empurrar o conteúdo para baixo do título fixo
st.markdown(f'<div style="padding-top: {PADDING_DO_TITULO_FIXO}px;">', unsafe_allow_html=True)

# Usamos enumerate para obter o índice (i) e a URL (link_produto)
for i, link_produto in enumerate(lista_de_urls):
    
    nome_produto = f"#{i + 1}" 
    
    # Header para cada produto
    st.markdown(f"""
    <div style="display: flex; align-items: baseline; gap: 15px; margin-top: 20px; margin-bottom: -10px;">
        <h2 style="margin-bottom: 0;">{nome_produto}</h2>
        <p style="margin-bottom: 0;"><strong>Link Original:</strong> <a href="{link_produto}" target="_blank">{link_produto}</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    html_content = f"""
    <iframe 
        src="{link_produto}" 
        width="{LARGURA_BASE_PIXELS}px" 
        height="{ALTURA_BASE_PIXELS}px"
        style="
            border: 1px solid #ccc; 
            transform: scale({FATOR_ZOOM}); 
            transform-origin: top left;
            margin-top: 20px;
        " 
    ></iframe>
    """

    st.components.v1.html(html_content, height=ALTURA_FINAL_STREAMLIT)
    
    # SEPARADOR VISUAL entre os produtos
    st.markdown("---")

st.markdown('</div>', unsafe_allow_html=True) # Fecha a div de padding

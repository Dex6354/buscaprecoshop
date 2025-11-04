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

# --- ESTRUTURA DE DADOS AJUSTADA ---
# Dicionário onde a chave é a URL e o valor é o preço fixo desejado (como string)
precos_fixos = {
    "https://www.centauro.com.br/bermuda-masculina-oxer-ls-basic-new-984889.html?cor=04": "R$ 79,90",
    "https://www.centauro.com.br/bermuda-masculina-oxer-mesh-mescla-983436.html?cor=MS": "R$ 50,00", # Exemplo que você forneceu
    "https://www.centauro.com.br/calcao-masculino-adams-liso-978059.html?cor=02": "R$ 129,99",
}
# --- FIM DA ESTRUTURA ---

# Título principal diminuído (usando h2 em vez de h1)
st.markdown("<h6>🛒 Preços Mercados</h6>", unsafe_allow_html=True)

# Usamos .items() para obter a URL (link_produto) e o preço (preco_desejado)
for i, (link_produto, preco_desejado) in enumerate(precos_fixos.items()):
    
    nome_produto = f"{i + 1}" # Você pode querer mudar isso para algo mais descritivo se a URL for longa
    
    # Usamos HTML/CSS (display: flex) para alinhar o número, o preço e a URL horizontalmente.
    st.markdown(f"""
    <div style="display: flex; align-items: baseline; gap: 15px; margin-bottom: -10px;">
        <h2 style="margin-bottom: 0;">{nome_produto})</h2>
        <p style="margin-bottom: 0; font-size: 1.2em; font-weight: bold; color: green;">
            {preco_desejado}
        </p>
        <p style="margin-bottom: 0; font-size: 0.8em; max-width: 600px; overflow-wrap: break-word;">
            <a href="{link_produto}" target="_blank">Acessar Produto</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    html_content = f"""
    <iframe 
        src="{link_produto}" 
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
    
    # SEPARADOR VISUAL entre os produtos
    st.markdown("---")

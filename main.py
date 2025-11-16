import streamlit as st
from urllib.parse import urlparse  # Usado para extrair o nome do site

# Configuração da página (layout 'wide' é ótimo para um dashboard)
st.set_page_config(
    layout="wide", 
    page_title="Monitor de Preços"
)

# Seu CSS para ocultar elementos do Streamlit (ótimo para um look 'limpo')
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

# Lista de produtos (sem alterações)
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
    ("R$ ", ""), # Este será ignorado
]

# Título principal (seu H6 funciona bem como um título sutil)
st.markdown("<h6>🔎 Monitor de Preço</h6>", unsafe_allow_html=True)

# --- NOVO LAYOUT EM GRADE ---

# 1. Defina o número de colunas
# 4 colunas parece um bom equilíbrio para 'wide' layout
N_COLS = 4
cols = st.columns(N_COLS)

# 2. Itere sobre os produtos e adicione-os às colunas
col_index = 0
for i, (preco_desejado, link_produto) in enumerate(precos_e_links):
    
    # Pula itens que não têm um link (como o seu último item da lista)
    if not link_produto.strip():
        continue

    # Seleciona a coluna correta, ciclando de 0 a 3 (índice % N_COLS)
    col = cols[col_index % N_COLS]

    # 3. Crie um "Card" dentro da coluna
    # `st.container(border=True)` cria uma caixa visualmente separada
    with col:
        with st.container(border=True):
            
            # Limpa o texto do preço para exibição
            display_price = preco_desejado.strip()
            # Se o preço for apenas "R$ ", exibe uma mensagem melhor
            if display_price.upper() == "R$":
                display_price = "Preço a verificar"
            
            # Título do Card
            st.markdown(f"**Item {i + 1}**")
            
            # Preço/Descrição em destaque
            # `st.subheader` dá um bom peso visual
            st.subheader(display_price)
            
            # Adiciona contexto (de qual site é)
            try:
                domain = urlparse(link_produto).hostname
                if domain.startswith('www.'):
                    domain = domain[4:] # Remove o 'www.'
                st.caption(f"em {domain}") # Mostra "em centauro.com.br"
            except Exception:
                st.caption("Link externo") # Fallback
            
            # 4. Botão de Ação
            # `st.link_button` é perfeito para isso e muito mais limpo
            st.link_button(
                "Acessar Produto", 
                link_produto, 
                use_container_width=True # Botão ocupa a largura do card
            )
            
    # Incrementa o índice para a próxima coluna
    col_index += 1

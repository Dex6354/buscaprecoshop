import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    layout="wide", 
    page_title="Monitor de Preços - Embed Centauro"
)

# --- CONFIGURAÇÕES DE AJUSTE ---
# 1. Largura do iFrame (Ajuste este valor, ex: 400px ou 50% do contêiner Streamlit)
LARGURA_IFRAME_PIXELS = "400px" # Define um valor fixo para ver o espaço à esquerda
ALTURA_IFRAME = 500  # Altura em pixels
BUFFER_ALTURA_STREAMLIT = 30 # Buffer

# 2. Posição da Rolagem (Em pixels, de cima para baixo. Ex: 300px)
SCROLL_POSITION = 300 
# -------------------------------


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

    # --- HTML/CSS/JS CUSTOMIZADO ---
    
    # 1. CSS e HTML para alinhamento e largura
    # Usamos float: right para mover o iframe para a direita.
    # Definimos a largura desejada (LARGURA_IFRAME_PIXELS) e altura.
    iframe_style = f"""
    style="
        width: {LARGURA_IFRAME_PIXELS}; 
        height: {ALTURA_IFRAME}px; 
        float: right; /* Move o iframe para a direita */
        border: 1px solid #ccc; /* Borda opcional para melhor visualização */
    "
    """
    
    # 2. JavaScript para rolar a página do iframe
    # Este script é executado DENTRO do contexto do iframe.
    # Ele espera que o conteúdo do iframe carregue (onload) e então rola para a posição desejada.
    scroll_script = f"""
    <script>
        const iframe = document.getElementById('product_iframe_{i}');
        
        // Função para rolar o conteúdo DO IFRAME para baixo
        function scrollToPosition() {{
            if (iframe && iframe.contentWindow) {{
                iframe.contentWindow.scrollTo(0, {SCROLL_POSITION});
            }} else {{
                // Tenta novamente se não carregou imediatamente
                setTimeout(scrollToPosition, 500); 
            }}
        }}
        
        // É difícil garantir o carregamento exato de um site externo como a Centauro.
        // Uma abordagem mais simples (e às vezes a única que funciona) é tentar rolar
        // APENAS o container do Streamlit, MAS VOCÊ PEDIU PARA ROLAR O EMBED.
        // A forma correta é no onload do iframe.
        
        // Para sites externos, a regra de Same-Origin Policy impede o script JS 
        // injetado no Streamlit de acessar o DOM interno do iframe.
        // A melhor alternativa é tentar adicionar um fragmento de URL (se o site suportar)
        // ou confiar apenas no scroll do navegador que o usuário fará.
        
        // **Como o script direto não funcionará por causa de segurança (Same-Origin Policy):**
        // Vamos tentar a técnica do fragmento de URL, que é mais universal, 
        // mas pode não funcionar se a Centauro não estiver configurada para isso.
        
        // Se você puder usar um URL que suporte scroll, seria assim (exemplo: ancoragem):
        // link_com_scroll = "{link_produto.split('#')[0]}#bottom"
        // Exemplo com um parâmetro de URL que algum sistema pode interpretar:
        // link_com_scroll = f"{{link_produto}}?scroll_to={SCROLL_POSITION}"
        
        // Como estamos presos, vamos apenas focar no layout e deixar o usuário rolar o iframe.
    </script>
    """
    
    # Monta o iFrame com ID para referência no script (embora o script não funcione totalmente)
    # Usamos 'scrolling="yes"' para garantir que o iframe tenha sua própria barra de rolagem.
    html_content = f"""
    <div style="overflow: hidden;"> <iframe 
            id="product_iframe_{i}" 
            src="{link_produto}" 
            {iframe_style}
            scrolling="yes"
        ></iframe>
    </div>
    {scroll_script}
    """

    # Exibe o componente HTML/iFrame
    # O height deve ser a altura do iframe + espaço extra se necessário.
    st.components.v1.html(html_content, height=ALTURA_IFRAME + 50) 
    
    # SEPARADOR VISUAL entre os produtos
    st.markdown("---")

# Nota Importante para o Usuário
st.warning("""
**Nota sobre a Rolagem Automática:** Devido às políticas de segurança do navegador (**Same-Origin Policy**), o código Streamlit não consegue injetar um script JavaScript diretamente no conteúdo de um site externo (como a Centauro) para forçar a rolagem para baixo no `iframe`. **O layout com o embed à direita funcionará, mas a rolagem automática pode não ocorrer.** O usuário precisará rolar manualmente dentro do *embed*.
""")

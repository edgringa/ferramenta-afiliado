import streamlit as st
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Configuração da Página
st.set_page_config(page_title="EuroAffiliate Ultimate", page_icon="🎛️", layout="wide")

st.title("🎛️ EuroAffiliate Ultimate - Painel de Controle de Alta Conversão")
st.markdown("---")

# Abas para organizar todas as funções que conversamos
aba1, aba2, aba3 = st.tabs([
    "🔑 Palavras-Chave de Ouro", 
    "🕵️ Espião Técnico & Subtítulos", 
    "🔗 Rastreador de Links do Rival"
])

# ----------------- ABA 1: PALAVRAS-CHAVE DE OURO & PERGUNTAS -----------------
with aba1:
    st.header("1. Mineração de Termos de Compra e Dúvidas (Mercado Europeu)")
    
    col1, col2 = st.columns(2)
    with col1:
        produto = st.text_input("Digite o produto ou nicho base (Ex: Nourix, coffee machine):", "", key="prod")
    with col2:
        mercado = st.selectbox(
            "Selecione o Mercado Alvo:",
            options=["en", "es", "de", "fr", "it"],
            format_func=lambda x: {"en": "Reino Unido / Global (EN)", "es": "Espanha (ES)", "de": "Alemanha (DE)", "fr": "França (FR)", "it": "Itália (IT)"}[x],
            key="merc"
        )
    
    if st.button("Gerar Inteligência de Conteúdo", key="btn_palavras"):
        if produto:
            # Modificadores de compra e modificadores de perguntas informativas
            modificadores = {
                "en": ["best", "review", "buy", "price", "how to", "is it safe", "side effects"],
                "es": ["mejor", "opiniones", "comprar", "precio", "como usar", "funciona", "contraindicaciones"],
                "de": ["beste", "test", "kaufen", "preis", "wie funktioniert", "erfahrungen", "nebenwirkungen"],
                "fr": ["meilleur", "avis", "acheter", "prix", "comment utiliser", "danger", "effets secondaires"],
                "it": ["migliore", "recensione", "comprare", "prezzo", "come assumere", "funziona", "effetti collaterali"]
            }
            
            sugestoes_finais = set()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            with st.spinner("Extraindo variações comerciais diretas do Google..."):
                # Busca o termo puro
                url_pura = f"https://google.com{mercado}&q={produto}"
                res = requests.get(url_pura, headers=headers)
                if res.status_code == 200:
                    for item in json.loads(res.text)[1]:
                        sugestoes_finais.add(item)
                
                # Busca variações com modificadores de compra e perguntas
                for mod in modificadores[mercado]:
                    url_mod = f"https://google.com{mercado}&q={produto} {mod}"
                    url_mod_antes = f"https://google.com{mercado}&q={mod} {produto}"
                    
                    for u in [url_mod, url_mod_antes]:
                        res_mod = requests.get(u, headers=headers)
                        if res_mod.status_code == 200:
                            for item in json.loads(res_mod.text)[1]:
                                sugestoes_finais.add(item)
            
            st.success(f"Sucesso! Encontramos ideias valiosas para estruturar sua estratégia.")
            
            lista_ordenada = sorted(list(sugestoes_finais))
            col_esq, col_dir = st.columns(2)
            meio = len(lista_ordenada) // 2
            
            with col_esq:
                st.subheader("🎯 Termos de Intenção Comercial / Dúvidas")
                for termo in lista_ordenada[:meio]:
                    st.write(f"• **{termo}**")
            with col_dir:
                st.subheader("🎯 Mais Variações Encontradas")
                for termo in lista_ordenada[meio:]:
                    st.write(f"• **{termo}**")
        else:
            st.warning("Por favor, digite o nome de um produto!")

# ----------------- ABA 2: ESPIÃO TÉCNICO & SUBTÍTULOS -----------------
with aba2:
    st.header("2. Anatomia de Conteúdo do Concorrente")
    url_concorrente = st.text_input("Cole a URL do rival europeu aqui:", "https://", key="url_espiao")
    
    if st.button("Dissecá-lo", key="btn_espiao"):
        if url_concorrente and url_concorrente != "https://":
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                resposta = requests.get(url_concorrente, headers=headers, timeout=10)
                
                if resposta.status_code == 200:
                    soup = BeautifulSoup(resposta.text, 'html.parser')
                    
                    # Status e Servidor
                    st.success(f"Status: 200 OK | Servidor Detectado: {resposta.headers.get('Server', 'Nginx/Cloudflare alternative')}")
                    
                    # Título de SEO
                    titulo = soup.title.string if soup.title else "Sem título"
                    st.markdown(f"#### 📋 Título de SEO ({len(titulo)} caracteres):\n> **{titulo}**")
                    if len(titulo) > 60:
                        st.warning("⚠️ Este título está muito longo! O Google pode cortar no navegador.")
                    
                    # Meta Description
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    desc_conteudo = meta_desc['content'] if meta_desc else "Ausente"
                    st.markdown(f"#### 📑 Descrição de SEO:\n> *{desc_conteudo}*")
                    
                    # Estrutura H2 e H3
                    st.markdown("#### 🧱 Esqueleto do Artigo (Subtítulos H2 e H3):")
                    subtitulos = soup.find_all(['h2', 'h3'])
                    for sub in subtitulos[:20]:
                        st.write(f"**[{sub.name.upper()}]** {sub.text.strip()}")
                else:
                    st.error(f"Erro ao acessar o site. Código HTTP: {resposta.status_code}")
            except Exception as e:
                st.error(f"Não foi possível ler este domínio. Detalhes: {e}")

# ----------------- ABA 3: RASTREADOR DE LINKS -----------------
with aba3:
    st.header("3. Desmascarar Links de Afiliados do Rival")
    st.caption("Esta função lê a página do concorrente e encontra para onde ele direciona os cliques de vendas.")
    
    url_links = st.text_input("Cole a mesma URL do concorrente para mapear os links:", "https://", key="url_links")
    
    if st.button("Rastrear Links Externos", key="btn_links"):
        if url_links and url_links != "https://":
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                resposta = requests.get(url_links, headers=headers, timeout=10)
                
                if resposta.status_code == 200:
                    soup = BeautifulSoup(resposta.text, 'html.parser')
                    dominio_base = urlparse(url_links).netloc
                    
                    links_externos = []
                    for a_tag in soup.find_all('a', href=True):
                        href = a_tag['href']
                        url_completa = urljoin(url_links, href)
                        dominio_destino = urlparse(url_completa).netloc
                        
                        # Verifica se o link joga para fora do próprio site do rival
                        if dominio_destino and dominio_destino != dominio_base:
                            texto_link = a_tag.text.strip() or "[Imagem ou Botão]"
                            links_externos.append((texto_link, url_completa))
                    
                    if links_externos:
                        st.success(f"Encontramos {len(links_externos)} links saindo dessa página!")
                        for texto, link_ext in links_externos:
                            # Tenta identificar plataformas famosas no link
                            plataforma = "Desconhecida / Direta"
                            if "amazon" in link_ext: plataforma = "📦 Amazon Affiliates"
                            elif "awin" in link_ext: plataforma = "🌐 Awin Network"
                            elif "clickbank" in link_ext: plataforma = "💥 ClickBank"
                            
                            st.write(f"🔗 **Texto do Botão:** `{texto}`")
                            st.write(f"➡️ **Destino Real:** `{link_ext}` | **Filtro:** {plataforma}")
                            st.markdown("---")
                    else:
                        st.warning("Não foram encontrados links direcionando para fora deste site.")
            except Exception as e:
                st.error(f"Erro ao analisar links: {e}")

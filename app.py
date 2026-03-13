import streamlit as st
import pandas as pd
import sys
import os

# Garante que o Python encontre os arquivos na raiz
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importações seguras
import database
import auth

# Configurações iniciais
st.set_page_config(page_title="Arquitetura de Linguagens", layout="wide")
database.inicializar_banco()

if auth.verificar_acesso():
    st.title("🌐 Sistema de Arquitetura de Linguagens")
    
    tab1, tab2, tab3 = st.tabs(["📚 Linguagens", "🔗 Relacionamentos", "💡 Recomendações"])

    with tab1:
        st.header("Microsserviço de Linguagens")
        
        # Formulário de Cadastro
        with st.expander("➕ Adicionar Nova Linguagem"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome da Linguagem", key="nome")
                criador = st.text_input("Criador / Empresa", key="criador")
            with col2:
                ano = st.number_input("Ano de Lançamento", min_value=1950, max_value=2026, value=2024)
                dif = st.select_slider("Dificuldade", options=["Fácil", "Médio", "Difícil"])
            
            if st.button("Salvar no Banco"):
                if nome:
                    # Chamada explícita usando o módulo 'database'
                    database.salvar_linguagem(nome, criador, ano, dif)
                    st.success(f"Linguagem {nome} salva!")
                    st.rerun()
                else:
                    st.error("O nome é obrigatório.")

        st.divider()

        # Listagem de Dados
        dados = database.listar_linguagens()
        if dados:
            df = pd.DataFrame(dados, columns=["ID", "Nome", "Criador", "Ano", "Dificuldade"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("O banco de dados está vazio.")

    with tab2:
        st.header("Microsserviço de Relacionamentos")
        st.info("Em breve: Visualização de hierarquias.")

    with tab3:
        st.header("Microsserviço de Recomendação")
        st.info("Em breve: Algoritmo de sugestão.")
else:
    st.info("Por favor, faça o login no menu lateral para acessar o sistema.")

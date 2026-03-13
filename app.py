import streamlit as st
import pandas as pd
from auth import verificar_acesso
from database import inicializar_banco, listar_linguagens, salvar_linguagem

# Configurações iniciais
st.set_page_config(page_title="Arquitetura de Linguagens", layout="wide")
inicializar_banco()

if verificar_acesso():
    st.title("🌐 Sistema de Arquitetura de Linguagens")
    
    tab1, tab2, tab3 = st.tabs(["📚 Linguagens", "🔗 Relacionamentos", "💡 Recomendações"])

    with tab1:
        st.header("Microsserviço de Linguagens")
        
        # Formulário de Cadastro
        with st.expander("➕ Adicionar Nova Linguagem"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome da Linguagem")
                criador = st.text_input("Criador / Empresa")
            with col2:
                ano = st.number_input("Ano de Lançamento", min_value=1950, max_value=2026, value=2024)
                dif = st.select_slider("Dificuldade", options=["Fácil", "Médio", "Difícil"])
            
            if st.button("Salvar no Banco"):
                if nome:
                    salvar_linguagem(nome, criador, ano, dif)
                    st.success(f"Linguagem {nome} salva!")
                    st.rerun()
                else:
                    st.error("O nome é obrigatório.")

        st.divider()

        # Listagem de Dados
        dados = listar_linguagens()
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

import streamlit as st
import pandas as pd
import sys
import os

# Força o Python a reconhecer os arquivos na mesma pasta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import database
import auth

# Inicialização
st.set_page_config(page_title="Arquitetura de Linguagens", layout="wide")
database.inicializar_banco()

if auth.verificar_acesso():
    st.title("🌐 Sistema de Arquitetura de Linguagens")
    
    tab1, tab2, tab3 = st.tabs(["📚 Linguagens", "🔗 Relacionamentos", "💡 Recomendações"])

    with tab1:
        st.header("Microsserviço de Linguagens")
        
        with st.expander("➕ Adicionar Nova Linguagem"):
            c1, c2 = st.columns(2)
            with c1:
                nome_input = st.text_input("Nome da Linguagem")
                criador_input = st.text_input("Criador / Empresa")
            with c2:
                ano_input = st.number_input("Ano", min_value=1950, max_value=2026, value=2024)
                dif_input = st.select_slider("Dificuldade", options=["Fácil", "Médio", "Difícil"])
            
            if st.button("Confirmar Cadastro"):
                if nome_input:
                    database.salvar_linguagem(nome_input, criador_input, ano_input, dif_input)
                    st.success(f"{nome_input} salvo!")
                    st.rerun()
                else:
                    st.error("Digite o nome!")

        st.divider()
        lista = database.listar_linguagens()
        if lista:
            df = pd.DataFrame(lista, columns=["ID", "Nome", "Criador", "Ano", "Dificuldade"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum dado cadastrado.")

    with tab2:
        st.header("🔗 Relacionamentos")
        st.write("Módulo de Microsserviço de Hierarquia.")

    with tab3:
        st.header("💡 Recomendações")
        st.write("Módulo de Microsserviço de Recomendação.")
else:
    st.info("Faça login no menu lateral (admin / 123)")

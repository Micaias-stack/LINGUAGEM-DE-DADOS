import streamlit as st
import pandas as pd
import sys
import os
import google.generativeai as genai

# Garante que o Python encontre os outros arquivos (auth e database) na raiz
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import database
import auth

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Portal de Arquitetura", layout="wide", page_icon="🌐")
database.inicializar_banco()

# --- CONFIGURAÇÃO DA IA (GEMINI) ---
# MUITO IMPORTANTE: Cole sua API KEY entre as aspas abaixo
CHAVE_IA = "AIzaSyAuo0NCeifxlxn8jhvNEH7BwXQe3lHk32g" 

# Inicializamos a variável como None para evitar o erro "not defined"
model_ia = None 

if CHAVE_IA != AIzaSyAuo0NCeifxlxn8jhvNEH7BwXQe3lHk32g"" and CHAVE_IA.strip() != "":
    try:
        genai.configure(api_key=CHAVE_IA)
        # Usamos 'gemini-pro' para máxima compatibilidade
        model_ia = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.sidebar.error(f"Erro na configuração da IA: {e}")

# --- INTERFACE ---
if auth.verificar_acesso():
    st.title("🌐 Portal de Arquitetura de Linguagens")
    
    tab1, tab2, tab3 = st.tabs(["📚 Base de Dados", "🔗 Relacionamentos", "🤖 Consultoria IA"])

    # Aba 1: Banco de Dados
    with tab1:
        st.header("Microsserviço de Linguagens")
        with st.expander("➕ Adicionar Tecnologia"):
            c1, c2 = st.columns(2)
            with c1:
                nome = st.text_input("Nome")
                criador = st.text_input("Criador")
            with c2:
                ano = st.number_input("Ano", min_value=1950, max_value=2026, value=2024)
                dif = st.select_slider("Dificuldade", options=["Fácil", "Médio", "Difícil"])
            
            if st.button("Salvar no Banco"):
                if nome:
                    database.salvar_linguagem(nome, criador, ano, dif)
                    st.success(f"Registrado!")
                    st.rerun()

        st.divider()
        dados = database.listar_linguagens()
        if dados:
            df = pd.DataFrame(dados, columns=["ID", "Nome", "Criador", "Ano", "Dificuldade"])
            st.dataframe(df, use_container_width=True, hide_index=True)

    # Aba 2: Relacionamentos
    with tab2:
        st.header("🔗 Relacionamentos")
        st.info("Módulo de arquitetura em expansão.")

    # Aba 3: IA
    with tab3:
        st.header("🤖 Consultoria IA")
        
        if CHAVE_IA == "SUA_CHAVE_AQUI":
            st.warning("⚠️ Insira sua API KEY no código para habilitar a IA.")
        else:
            pergunta = st.text_area("Dúvida técnica:", placeholder="Ex: Por que Python é bom para IA?")
            
            if st.button("Consultar"):
                if pergunta and model_ia:
                    with st.spinner("IA processando..."):
                        try:
                            response = model_ia.generate_content(pergunta)
                            st.subheader("💡 Resposta:")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"Erro na resposta: {e}")
                elif not model_ia:
                    st.error("IA não inicializada. Verifique a chave.")
else:
    st.info("Aguardando login...")

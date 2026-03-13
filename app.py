import streamlit as st
import pandas as pd
import sys
import os
import google.generativeai as genai

# Configuração de Caminho para rodar no Streamlit Cloud
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import database
import auth

# Configuração da Página
st.set_page_config(page_title="Arquitetura Inteligente", layout="wide", page_icon="🤖")
database.inicializar_banco()

# --- CONFIGURAÇÃO DA IA ---
# COLE SUA CHAVE ENTRE AS ASPAS ABAIXO
CHAVE_IA = "SUA_CHAVE_AQUI" 

if CHAVE_IA != "SUA_CHAVE_AQUI":
    try:
        genai.configure(api_key=CHAVE_IA)
        # Usando 'gemini-pro' que tem maior compatibilidade v1
        model_ia = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Erro ao configurar IA: {e}")

if auth.verificar_acesso():
    st.title("🌐 Portal de Arquitetura de Linguagens")
    
    tab1, tab2, tab3 = st.tabs(["📚 Base de Dados", "🔗 Relacionamentos", "🤖 Consultoria IA"])

    with tab1:
        st.header("Microsserviço de Linguagens")
        with st.expander("➕ Cadastrar Nova Tecnologia"):
            c1, c2 = st.columns(2)
            with c1:
                nome = st.text_input("Nome")
                criador = st.text_input("Criador/Empresa")
            with c2:
                ano = st.number_input("Ano", min_value=1950, max_value=2026, value=2024)
                dif = st.select_slider("Dificuldade", options=["Fácil", "Médio", "Difícil"])
            
            if st.button("Salvar Tecnologia"):
                if nome:
                    database.salvar_linguagem(nome, criador, ano, dif)
                    st.success(f"{nome} salvo!")
                    st.rerun()

        st.divider()
        dados = database.listar_linguagens()
        if dados:
            df = pd.DataFrame(dados, columns=["ID", "Linguagem", "Criador", "Ano", "Dificuldade"])
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        st.header("🔗 Relacionamentos")
        st.info("Módulo de Microsserviços: Em breve visualização de grafos.")

    with tab3:
        st.header("🤖 Consultoria de Arquitetura")
        if CHAVE_IA == "AIzaSyAuo0NCeifxlxn8jhvNEH7BwXQe3lHk32g":
            st.warning("⚠️ IA não configurada. Coloque sua API KEY no arquivo app.py")
        else:
            pergunta = st.text_area("Descreva seu projeto ou dúvida técnica:", 
                                   placeholder="Ex: Como criar um arquivo em Python?")
            
            if st.button("Consultar Especialista Digital"):
                if pergunta:
                    with st.spinner("🤖 IA pensando..."):
                        try:
                            # Prompt para o Gemini
                            response = model_ia.generate_content(f"Responda de forma clara e técnica para um desenvolvedor: {pergunta}")
                            st.subheader("💡 Resposta da IA:")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"Erro na IA: {e}")
                else:
                    st.warning("Digite uma pergunta.")
else:
    st.info("Faça login no menu lateral para acessar.")

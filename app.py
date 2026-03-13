import streamlit as st
import pandas as pd
import sys
import os
import google.generativeai as genai

# Configuração de Caminho
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import database
import auth

# Configuração da Página
st.set_page_config(page_title="Arquitetura Inteligente", layout="wide", page_icon="🤖")
database.inicializar_banco()

# --- INTEGRAÇÃO COM IA ---
# Substitua pela sua chave do Google AI Studio
CHAVE_IA = "AIzaSyAuo0NCeifxlxn8jhvNEH7BwXQe3lHk32g" 
genai.configure(api_key=CHAVE_IA)
model_ia = genai.GenerativeModel('gemini-1.5-flash')

if auth.verificar_acesso():
    st.title("🌐 Portal de Arquitetura de Linguagens")
    
    tab1, tab2, tab3 = st.tabs(["📚 Base de Dados", "🔗 Relacionamentos", "🤖 Consultoria IA"])

    # --- ABA 1: GERENCIAMENTO ---
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
                    st.success(f"{nome} adicionado com sucesso!")
                    st.rerun()

        st.divider()
        dados = database.listar_linguagens()
        if dados:
            df = pd.DataFrame(dados, columns=["ID", "Linguagem", "Criador", "Ano", "Dificuldade"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("O banco de dados está vazio.")

    # --- ABA 2: RELACIONAMENTOS ---
    with tab2:
        st.header("Microsserviço de Relacionamentos")
        st.write("Aqui você verá a conexão entre as linguagens cadastradas.")
        st.warning("Módulo em fase de estruturação de grafos.")

    # --- ABA 3: INTELIGÊNCIA ARTIFICIAL ---
    with tab3:
        st.header("🤖 Consultoria de Arquitetura")
        st.write("Pergunte à IA qual a melhor linguagem para o seu objetivo.")
        
        pergunta = st.text_area("Descreva seu projeto ou dúvida técnica:", 
                               placeholder="Ex: Quero criar um sistema de IA para iPhone, qual linguagem uso?")
        
        if st.button("Consultar Especialista Digital"):
            if pergunta:
                if CHAVE_IA == "SUA_CHAVE_AQUI":
                    st.error("Por favor, configure sua API KEY no arquivo app.py")
                else:
                    with st.spinner("A IA está analisando sua requisição..."):
                        try:
                            prompt = f"Você é um arquiteto de software. Responda de forma curta: {pergunta}"
                            response = model_ia.generate_content(prompt)
                            st.subheader("💡 Recomendação da IA:")
                            st.info(response.text)
                        except Exception as e:
                            st.error(f"Erro na conexão com IA: {e}")
            else:
                st.warning("Digite uma pergunta para a IA.")

else:
    st.info("Utilize as credenciais no menu lateral para acessar o sistema.")

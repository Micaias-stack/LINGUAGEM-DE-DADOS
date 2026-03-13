import streamlit as st
import pandas as pd
import sys
import os
from groq import Groq

# Garante que o Python encontre os outros arquivos na raiz
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import database
import auth

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Portal de Arquitetura", layout="wide", page_icon="⚡")
database.inicializar_banco()

# --- CONFIGURAÇÃO DA IA (GROQ) ---
# COLE SUA CHAVE DO GROQ ABAIXO
CHAVE_GROQ = "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" 

client = None
if CHAVE_GROQ != "SUA_CHAVE_GROQ_AQUI" and CHAVE_GROQ.strip() != "":
    try:
        client = Groq(api_key=CHAVE_GROQ)
    except Exception as e:
        st.sidebar.error(f"Erro ao configurar Groq: {e}")

# --- INTERFACE ---
if auth.verificar_acesso():
    st.title("⚡ Consultoria de Arquitetura (Groq)")
    
    tab1, tab2, tab3 = st.tabs(["📚 Base de Dados", "🔗 Relacionamentos", "🤖 Consultoria Ultra Rápida"])

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
        lista = database.listar_linguagens()
        if lista:
            df = pd.DataFrame(lista, columns=["ID", "Nome", "Criador", "Ano", "Dificuldade"])
            st.dataframe(df, use_container_width=True, hide_index=True)

    # Aba 2: Relacionamentos
    with tab2:
        st.header("🔗 Relacionamentos")
        st.info("Módulo em expansão.")

    # Aba 3: IA com o novo Llama 3.3
    with tab3:
        st.header("🤖 Consultoria Inteligente")
        
        if CHAVE_GROQ == "SUA_CHAVE_GROQ_AQUI":
            st.warning("⚠️ Insira sua API KEY do Groq no arquivo app.py")
        else:
            pergunta = st.text_area("Sua dúvida técnica:", placeholder="Ex: Como criar um arquivo em Python?")
            
            if st.button("Consultar Groq"):
                if pergunta and client:
                    with st.spinner("Llama 3.3 processando..."):
                        try:
                            # Atualizado para o modelo Llama 3.3 Versatile
                            chat_completion = client.chat.completions.create(
                                messages=[{"role": "user", "content": pergunta}],
                                model="llama-3.3-70b-versatile",
                            )
                            st.subheader("💡 Resposta da IA:")
                            st.markdown(chat_completion.choices[0].message.content)
                        except Exception as e:
                            st.error(f"Erro no Groq: {e}")
                else:
                    st.warning("Digite algo.")
else:
    st.info("Acesse pelo menu lateral.")

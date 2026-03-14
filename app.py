import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
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
CHAVE_GROQ = "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" 

client = None
if CHAVE_GROQ.strip() != "" and CHAVE_GROQ != "SUA_CHAVE_GROQ_AQUI":
    try:
        client = Groq(api_key=CHAVE_GROQ)
    except Exception as e:
        st.sidebar.error(f"Erro ao configurar Groq: {e}")

# --- INTERFACE ---
if auth.verificar_acesso():
    st.title("⚡ Consultoria de Arquitetura (Groq)")
    
    # Abas organizadas: Dashboard, Base, Relacionamentos e IA
    tab0, tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📚 Base de Dados", "🔗 Relacionamentos", "🤖 Consultoria Ultra Rápida"])

    # Aba 0: Dashboard (Visualização de Dados)
    with tab0:
        st.header("Análise de Dados da Stack")
        lista_dados = database.listar_linguagens()
        
        if lista_dados:
            df_dash = pd.DataFrame(lista_dados, columns=["ID", "Nome", "Criador", "Ano", "Dificuldade"])
            
            col_d1, col_d2 = st.columns([1, 1])
            with col_d1:
                st.subheader("Distribuição por Dificuldade")
                fig_pie = px.pie(df_dash, names='Dificuldade', hole=.4, template="plotly_dark",
                                color_discrete_sequence=px.colors.qualitative.Safe)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col_d2:
                st.subheader("Novas Tecnologias por Ano")
                fig_hist = px.histogram(df_dash, x="Ano", template="plotly_dark", color_discrete_sequence=['#00CC96'])
                st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("Adicione tecnologias na 'Base de Dados' para ver as estatísticas.")

    # Aba 1: Banco de Dados
    with tab1:
        st.header("Microsserviço de Linguagens")
        with st.expander("➕ Adicionar Tecnologia", expanded=False):
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
            
            # Opção de limpar banco (Cuidado!)
            if st.button("Limpar Histórico (Reset)"):
                # Se seu database.py tiver uma função de deletar, chame aqui
                st.warning("Função de reset em implementação.")

    # Aba 2: Relacionamentos (Mapa de Grafo Interativo)
    with tab2:
        st.header("🔗 Mapa de Conexões")
        lista_rel = database.listar_linguagens()
        
        if len(lista_rel) > 1:
            nomes = [item[1] for item in lista_rel]
            n_nos = len(nomes)
            angulos = np.linspace(0, 2*np.pi, n_nos, endpoint=False)
            x_nos = np.cos(angulos)
            y_nos = np.sin(angulos)
            
            edge_x, edge_y = [], []
            for i in range(n_nos):
                for j in range(i + 1, n_nos):
                    edge_x.extend([x_nos[i], x_nos[j], None])
                    edge_y.extend([y_nos[i], y_nos[j], None])

            fig_grafo = px.scatter(x=x_nos, y=y_nos, text=nomes, template="plotly_dark")
            fig_grafo.update_traces(marker=dict(size=35, color='#FF4B4B'), textposition="top center", mode="markers+text")
            fig_grafo.add_scatter(x=edge_x, y=edge_y, mode="lines", line=dict(color="#555", width=1), showlegend=False)
            fig_grafo.update_layout(showlegend=False, height=450, 
                                   xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                   yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
            st.plotly_chart(fig_grafo, use_container_width=True)
        else:
            st.info("Adicione pelo menos 2 tecnologias para mapear os relacionamentos.")

    # Aba 3: IA Consultoria
    with tab3:
        st.header("🤖 Consultoria Inteligente (Llama 3.3)")
        analisar_banco = st.checkbox("Usar meus dados como contexto para a IA")
        pergunta = st.text_area("Sua dúvida técnica:", placeholder="Ex: Qual dessas tecnologias é melhor para escalabilidade?")
        
        if st.button("Consultar Groq"):
            if client and pergunta:
                with st.spinner("Analisando..."):
                    try:
                        contexto = ""
                        if analisar_banco:
                            dados = database.listar_linguagens()
                            contexto = f"\nMinha stack atual: {str(dados)}"

                        chat_completion = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": "Você é um arquiteto de dados. Analise a stack do usuário e dê conselhos práticos."},
                                {"role": "user", "content": pergunta + contexto}
                            ],
                            model="llama-3.3-70b-versatile",
                        )
                        st.subheader("💡 Resposta:")
                        st.markdown(chat_completion.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Erro: {e}")
            else:
                st.warning("Verifique a Chave ou a Pergunta.")
else:
    st.info("Acesse pelo menu lateral.")

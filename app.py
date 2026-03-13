import streamlit as st
# Note que agora importamos direto, sem o "utils." ou "data."
from auth import verificar_acesso
from database import inicializar_banco, listar_linguagens

# Inicializa o banco
inicializar_banco()

st.set_page_config(page_title="Arquitetura de Linguagens", layout="wide")

if verificar_acesso():
    st.title("🌐 Sistema de Arquitetura de Linguagens")
    
    tab1, tab2, tab3 = st.tabs(["📚 Linguagens", "🔗 Relacionamentos", "💡 Recomendações"])

        with tab1:
        st.header("Microsserviço de Linguagens")
        
        # Formulário para adicionar novas linguagens
        with st.expander("➕ Adicionar Nova Linguagem"):
            nome = st.text_input("Nome da Linguagem")
            criador = st.text_input("Criador / Empresa")
            ano = st.number_input("Ano de Lançamento", min_value=1950, max_value=2026, value=2024)
            dif = st.select_slider("Nível de Dificuldade", options=["Fácil", "Médio", "Difícil"])
            
            if st.button("Salvar no Banco"):
                if nome:
                    from database import salvar_linguagem
                    salvar_linguagem(nome, criador, ano, dif)
                    st.success(f"{nome} cadastrada com sucesso!")
                    st.rerun() # Atualiza a página para mostrar os dados
                else:
                    st.error("O nome da linguagem é obrigatório.")

        # Exibição dos dados
        st.divider()
        dados = listar_linguagens()
        if dados:
            import pandas as pd
            # Transformamos em DataFrame para ficar bonito no mobile
            df = pd.DataFrame(dados, columns=["ID", "Nome", "Criador", "Ano", "Dificuldade"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("O banco de dados está vazio.")


    with tab2:
        st.header("Microsserviço de Relacionamentos")
        st.write("Mapeamento de influências.")

    with tab3:
        st.header("Microsserviço de Recomendação")
        st.write("Módulo de sugestões.")
else:
    st.info("Acesse com 'admin' e senha '123' no menu lateral.")

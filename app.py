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
        dados = listar_linguagens()
        if dados:
            st.table(dados)
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

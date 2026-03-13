import streamlit as st
from utils.auth import verificar_acesso
from data.database import inicializar_banco, listar_linguagens

# Inicializa as tabelas se não existirem
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
            st.info("O banco de dados está vazio. Adicione linguagens via código ou painel admin.")

    with tab2:
        st.header("Microsserviço de Relacionamentos")
        st.write("Módulo de hierarquia e influências.")

    with tab3:
        st.header("Microsserviço de Recomendação")
        st.write("Módulo de sugestões personalizadas.")
else:
    st.info("Acesse com 'admin' e senha '123' no menu lateral para visualizar os dados.")

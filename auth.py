import streamlit as st

def verificar_acesso():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    with st.sidebar:
        st.title("🔐 Segurança")
        if not st.session_state.autenticado:
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            if st.button("Login"):
                if usuario == "admin" and senha == "123":
                    st.session_state.autenticado = True
                    st.session_state.role = "admin"
                    st.rerun()
                else:
                    st.error("Credenciais inválidas")
        else:
            st.write(f"Logado como: **{st.session_state.role}**")
            if st.button("Sair"):
                st.session_state.autenticado = False
                st.rerun()
    
    return st.session_state.autenticado

import streamlit as st
import random
from RSA import RSA

st.title("Application RSA")
st.write("""Cette application vous permet de crypter et de décrypter un message en utilisant des clés RSA.""")


n_max = st.sidebar.number_input("Valeur maximale pour les nombres premiers (n_max)", min_value=10, max_value=1000, value=100, step=10)
rsa = RSA(n_max=n_max)

# Génération des clés RSA
if 'cles_generees' not in st.session_state:
    st.session_state['cles_generees'] = False

if st.sidebar.button("Générer les clés RSA"):
    try:
        e, d, n = rsa.generer_cles()
        st.session_state['e'] = e
        st.session_state['d'] = d
        st.session_state['n'] = n
        st.session_state['cles_generees'] = True
        st.success("Clés générées avec succès !")
    except Exception as ex:
        st.error(f"Erreur lors de la génération des clés : {ex}")

# Crypter le message
if st.session_state['cles_generees']:
    # Interface pour crypter
    message_a_crypter = st.text_input("Entrez le message à crypter :", value="Bonjour")
    if st.button("Crypter"):
        if message_a_crypter:
            message_crypte = rsa.crypter(message_a_crypter, st.session_state['e'], st.session_state['n'])
            st.write(f"**Message crypté** : {message_crypte}")
        else:
            st.warning("Veuillez entrer un message à crypter.")

    st.markdown("---")

    # Décrypter le message
    message_a_decrypter = st.text_input("Entrez le message crypté :", value="")
    if st.button("Décrypter"):
        if message_a_decrypter:
            try:
                message_decrypte = rsa.decrypter(message_a_decrypter, st.session_state['d'], st.session_state['n'])
                st.write(f"**Message décrypté** : {message_decrypte}")
            except Exception as ex:
                st.error(f"Erreur lors du décryptage : {ex}")
        else:
            st.warning("Veuillez entrer un message crypté à décrypter.")

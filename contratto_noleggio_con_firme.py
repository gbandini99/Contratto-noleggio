
import streamlit as st
from fpdf import FPDF
from PIL import Image
import datetime
import os

st.title("Generatore Contratto Noleggio Carrello Moto – con firme")

st.header("Dati del Conduttore")
nome = st.text_input("Nome e Cognome")
nascita = st.text_input("Data di nascita (es. 01/01/1990)")
residenza = st.text_input("Residenza")
cf = st.text_input("Codice Fiscale")

st.header("Dati del Noleggio")
targa = st.text_input("Targa del carrello")
data_inizio = st.text_input("Data inizio noleggio")
data_fine = st.text_input("Data fine noleggio")
ora_restituzione = st.text_input("Ora restituzione")
prezzo = st.text_input("Prezzo del noleggio (EUR)")
cauzione = st.text_input("Cauzione richiesta (EUR)")

st.header("Luogo e Firma")
luogo = st.text_input("Luogo di firma")
data_firma = st.text_input("Data di firma")

firma_locatore = st.file_uploader("Carica firma Locatore (PNG/JPG)", type=["png", "jpg", "jpeg"])
firma_conduttore = st.file_uploader("Carica firma Conduttore (PNG/JPG)", type=["png", "jpg", "jpeg"])

if st.button("Genera Contratto PDF"):
    if not all([nome, nascita, residenza, cf, targa, data_inizio, data_fine,
                ora_restituzione, prezzo, cauzione, luogo, data_firma, firma_locatore, firma_conduttore]):
        st.error("⚠️ Per favore compila tutti i campi e carica entrambe le firme.")
    else:
        st.success("Contratto generato correttamente (placeholder, codice completo in versione finale).")

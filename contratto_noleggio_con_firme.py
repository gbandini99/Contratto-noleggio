import streamlit as st
from fpdf import FPDF
import datetime

def sanitize(text):
    return (
        text.replace("“", "\"")
            .replace("”", "\"")
            .replace("–", "-")
            .replace("’", "'")
            .replace("•", "-")
            .replace("é", "e")
            .replace("à", "a")
            .replace("è", "e")
            .replace("ì", "i")
            .replace("ò", "o")
            .replace("ù", "u")
    )

st.title("Generatore Contratto Noleggio Carrello Moto – PDF firmabile")

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
luogo = st.text_input("Luogo di firma")

if st.button("Genera Contratto PDF"):
    if not all([nome, nascita, residenza, cf, targa, data_inizio, data_fine, ora_restituzione, prezzo, cauzione, luogo]):
        st.error("⚠️ Compila tutti i campi per generare il contratto.")
    else:
        now = datetime.datetime.now()
        data_firma = now.strftime("%d/%m/%Y")
        ora_firma = now.strftime("%H:%M")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, sanitize("CONTRATTO DI NOLEGGIO TRA PRIVATI - CARRELLO PORTA MOTO"), ln=True, align='C')
        pdf.ln(10)

        testo = f"""
Tra i sottoscritti:

- Il Sig. Giacomo Bandini, nato il 23/02/1999, residente in via Laghi 57/2, C.F. BNDGCM99B23D458O, di seguito denominato "Locatore";

e

- Il Sig./la Sig.ra {nome}, nato/a il {nascita}, residente in {residenza}, C.F. {cf}, in possesso di patente di guida valida e della carta di circolazione del veicolo trainante, di seguito denominato/a "Conduttore";

Si stipula il seguente contratto di noleggio:

Il Locatore concede in uso temporaneo al Conduttore il carrello porta moto targato {targa}, per il trasporto di motocicli.

Periodo di noleggio:
dal {data_inizio} al {data_fine}, con restituzione prevista entro le ore {ora_restituzione} del giorno {data_fine}.

Il corrispettivo per il noleggio è pari a EUR {prezzo}, da versare anticipatamente. È inoltre richiesta una cauzione di EUR {cauzione}, che verrà restituita al termine del noleggio salvo danni o inadempienze.

Il Conduttore si impegna a:
- Utilizzare il carrello in conformità alle norme del Codice della Strada
- Restituire il carrello nelle stesse condizioni in cui è stato ricevuto
- Assumersi ogni responsabilità civile e penale derivante dall'uso del mezzo

Il Locatore declina ogni responsabilità per danni a persone o cose derivanti dall'uso improprio del carrello da parte del Conduttore.

Letto, approvato e sottoscritto.

Luogo: {luogo}
Data: {data_firma}
Ora: {ora_firma}

Firma del Locatore: ______________________

Firma del Conduttore: ______________________
        """

        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 10, sanitize(testo))
        path_out = "contratto_noleggio.pdf"
        pdf.output(path_out)

        with open(path_out, "rb") as f:
            st.download_button("📄 Scarica il contratto PDF", f, file_name=path_out, mime="application/pdf")
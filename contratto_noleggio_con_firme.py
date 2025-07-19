
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
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=11)

        # Intestazione
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "CONTRATTO DI NOLEGGIO TRA PRIVATI – CARRELLO PORTA MOTO", ln=True, align='C')
        pdf.set_font("Arial", size=11)
        pdf.ln(10)

        pdf.multi_cell(0, 10, f"Tra i sottoscritti:

"
                              f"- Il Sig. Giacomo Bandini, nato il 23/02/1999, residente in via Laghi 57/2, C.F. BNDGCM99B23D458O, di seguito denominato “Locatore”;

"
                              f"e

"
                              f"- Il Sig./la Sig.ra {nome}, nato/a il {nascita}, residente in {residenza}, C.F. {cf}, in possesso di patente di guida valida e della carta di circolazione del veicolo trainante, di seguito denominato/a “Conduttore”;")

        pdf.multi_cell(0, 10, f"Art. 1 – Oggetto del Contratto
"
                              f"Il Locatore concede in noleggio al Conduttore, che accetta, un carrello porta moto omologato per 3 posti, targato {targa}, di proprietà del Locatore.")

        pdf.multi_cell(0, 10, f"Art. 2 – Durata del Noleggio
"
                              f"Il presente contratto ha durata dal giorno {data_inizio} al giorno {data_fine}. "
                              f"Il carrello dovrà essere restituito entro le ore {ora_restituzione} del giorno di scadenza, salvo diverso accordo scritto tra le parti.")

        pdf.multi_cell(0, 10, f"Art. 3 – Corrispettivo
"
                              f"Il canone di noleggio concordato è pari a EUR {prezzo}, da versarsi in un’unica soluzione al momento della consegna del carrello.
"
                              f"A garanzia dell’integrità del bene, è richiesta una cauzione di EUR {cauzione}, che sarà restituita al momento della riconsegna, previa verifica dell’integrità del carrello.")

        pdf.multi_cell(0, 10, "Art. 4 – Obblighi del Conduttore
"
                              "- utilizzare il carrello esclusivamente per il trasporto di motocicli;
"
                              "- non cedere a terzi l’uso del carrello;
"
                              "- custodire il carrello con diligenza;
"
                              "- utilizzare il carrello solo con veicoli trainanti omologati e con carta di circolazione valida;
"
                              "- rispettare il Codice della Strada e ogni normativa vigente.")

        pdf.multi_cell(0, 10, "Art. 5 – Responsabilità
"
                              "Il Conduttore è l’unico responsabile per eventuali danni a cose o persone derivanti dall’uso del carrello durante il periodo di noleggio.
"
                              "Il Locatore è esonerato da qualsiasi responsabilità per:
"
                              "- infrazioni al Codice della Strada;
"
                              "- incidenti o sinistri causati dal carrello durante l’uso;
"
                              "- furti o danni derivanti da negligenza del Conduttore.")

        pdf.multi_cell(0, 10, "Art. 6 – Stato del Bene
"
                              "Il carrello viene consegnato in buono stato e perfettamente funzionante. Le parti eseguono un controllo visivo al momento della consegna e della riconsegna. "
                              "Eventuali danni riscontrati al termine del noleggio saranno a carico del Conduttore.")

        pdf.multi_cell(0, 10, "Art. 7 – Foro Competente
"
                              "Per qualsiasi controversia relativa all’interpretazione o all’esecuzione del presente contratto è competente in via esclusiva il Foro di Faenza.")

        pdf.ln(10)
        pdf.multi_cell(0, 10, f"{luogo}, {data_firma}

"
                              f"Il Locatore                          Il Conduttore")

        # Salva PDF temporaneamente
        output_path = "contratto_noleggio_firmato.pdf"
        pdf.output(output_path)

        # Ora aggiungiamo le firme grafiche
        from PyPDF2 import PdfReader, PdfWriter
        from PyPDF2.pdf import PageObject
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        import io

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)

        if firma_locatore:
            img_loc = Image.open(firma_locatore)
            loc_path = "firma_locatore.png"
            img_loc.save(loc_path)
            can.drawImage(loc_path, 80, 130, width=80, height=40)

        if firma_conduttore:
            img_con = Image.open(firma_conduttore)
            con_path = "firma_conduttore.png"
            img_con.save(con_path)
            can.drawImage(con_path, 150, 130, width=80, height=40)

        can.save()
        packet.seek(0)

        # Merge firme sul PDF
        existing_pdf = PdfReader(output_path)
        overlay = PdfReader(packet)
        writer = PdfWriter()
        page = existing_pdf.pages[0]
        page.merge_page(overlay.pages[0])
        writer.add_page(page)

        final_pdf_path = "Contratto_Noleggio_Firmato_ConFirme.pdf"
        with open(final_pdf_path, "wb") as f_out:
            writer.write(f_out)

        with open(final_pdf_path, "rb") as f:
            st.download_button("📄 Scarica il PDF firmato", f, file_name=final_pdf_path, mime="application/pdf")

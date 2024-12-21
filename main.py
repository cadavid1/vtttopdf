import streamlit as st
from pathlib import Path
from fpdf import FPDF
import webvtt

# Function to convert a single VTT file to PDF
def vtt_to_pdf(vtt_file_path, output_pdf_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for caption in webvtt.read(vtt_file_path):
        pdf.multi_cell(0, 10, f"{caption.start} --> {caption.end}\n{caption.text}\n")

    pdf.output(output_pdf_path)

# Streamlit app
st.title("VTT to PDF Converter")
st.write("Upload your VTT files, and download them as PDFs.")

# File uploader for multiple VTT files
uploaded_files = st.file_uploader("Upload VTT files", accept_multiple_files=True, type=["vtt"])

if uploaded_files:
    output_files = []
    output_folder = Path("converted_pdfs")
    output_folder.mkdir(exist_ok=True)

    for uploaded_file in uploaded_files:
        vtt_file_path = Path(uploaded_file.name)
        vtt_file_path.write_bytes(uploaded_file.getvalue())

        output_pdf_path = output_folder / (vtt_file_path.stem + ".pdf")
        vtt_to_pdf(vtt_file_path, output_pdf_path)
        output_files.append(output_pdf_path)

    # Provide download links for the converted PDFs
    st.success("Conversion completed! Download your PDFs below:")
    for output_file in output_files:
        with open(output_file, "rb") as f:
            st.download_button(
                label=f"Download {output_file.name}",
                data=f,
                file_name=output_file.name,
                mime="application/pdf"
            )

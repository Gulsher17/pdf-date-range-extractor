import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import datetime
import io
import re

def filter_pdf_by_date_range(file, start_date, end_date):
    reader = PdfReader(file)
    writer = PdfWriter()
    date_regex = re.compile(r"\d{2}/\d{2}/\d{4}")  # Matches MM/DD/YYYY

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            matches = date_regex.findall(text)
            for match in matches:
                try:
                    date = datetime.datetime.strptime(match, "%m/%d/%Y").date()
                    if start_date <= date <= end_date:
                        writer.add_page(page)
                        break
                except:
                    pass

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return output

# --- Streamlit UI ---
st.set_page_config(page_title="PDF Date Extractor", layout="centered")

st.title("📄 PDF Date Range Extractor")
st.markdown("Upload a PDF file, select a date range, and extract pages with dates in that range.")

uploaded = st.file_uploader("Upload PDF", type="pdf")
start = st.date_input("Start Date", value=datetime.date(2025, 3, 20))
end = st.date_input("End Date", value=datetime.date(2025, 3, 27))

if uploaded and st.button("Extract Pages"):
    with st.spinner("Extracting matching pages..."):
        output = filter_pdf_by_date_range(uploaded, start, end)
        st.success("✅ Extraction Complete!")
        st.download_button("📥 Download Filtered PDF", output, file_name="filtered_by_date.pdf", mime="application/pdf")

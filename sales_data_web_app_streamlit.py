
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pandas.plotting import table

def process_sales_data(dataframe):
    # Calculate average sales per article
    average_sales = dataframe.groupby('Artikel')['Menge'].mean().reset_index()
    average_sales.rename(columns={'Menge': 'Durchschnittliche Menge pro Woche'}, inplace=True)
    
    # Retain original order of articles
    sorted_sales = dataframe[['Artikel', 'Name']].drop_duplicates().merge(
        average_sales, on='Artikel', how='left'
    )
    return sorted_sales

st.title("Berechnung der durchschnittlichen Abverkäufe")
st.write("Bitte laden Sie eine Excel-Datei hoch, um die durchschnittlichen Verkäufe pro Woche zu berechnen.")

# File uploader
uploaded_file = st.file_uploader("Bitte laden Sie Ihre Excel-Datei hoch", type=["xlsx"])
if uploaded_file:
    # Load the Excel file
    data = pd.ExcelFile(uploaded_file)
    sheet_name = data.sheet_names[0]  # Assume the first sheet is relevant
    df = data.parse(sheet_name)
    
    # Process data
    result = process_sales_data(df)
    
    # Show results
    st.write("Ergebnisse:")
    st.dataframe(result)
    
    # Download results
    output_file = "durchschnittliche_abverkaeufe.xlsx"
    result.to_excel(output_file, index=False)
    with open(output_file, "rb") as file:
        st.download_button("Laden Sie die Ergebnisse herunter", file, file_name=output_file)

# Add a disclaimer and credit at the bottom of the page
st.markdown("---")
st.markdown(
    "⚠️ **Hinweis:** Diese Anwendung speichert keine Daten und hat keinen Zugriff auf Ihre Dateien. "
    "Alle Verarbeitungen erfolgen lokal auf Ihrem Gerät oder auf dem temporären Streamlit-Server."
)
st.markdown(
    "🌟 **Erstellt von Christoph R. Kaiser mit Hilfe von Künstlicher Intelligenz.**"
)

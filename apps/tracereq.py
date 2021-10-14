import streamlit as st, pandas as pd
from traceability.preprocessing_evaluation import prosesData
from traceability.lda import latentDirichlet
from traceability.lsa import latentSemantic
from traceability.vsm import measurement

def app():
    st.header("tracereq Module")
    st.markdown("Modul usulan ini digunakan untuk melihat kebergantungan kebutuhan berdasarkan ekspart")

    dataset1 = st.file_uploader("Choose a file", key= 'ekspart') 
    if dataset1 is None:
        st.warning("masukkan data terlebih dahulu")

    elif dataset1 is not None:
        st.sidebar.header('Dataset Test Parameter')
        x1 = pd.ExcelFile(dataset1)
        srs_param = st.sidebar.selectbox( 'What Dataset you choose?', x1.sheet_names)
        myProses = prosesData(dataset1)
        data_raw = myProses.fulldataset(srs_param)['Requirement Statement']
        st.write(data_raw)
        # data_bersih = myProses.clean_text(data_raw)
        # measurement(myProses).bagOfWords()
        # st.write(myProses)


import streamlit as st, pandas as pd
from tracereq.preprocessing_evaluation import prosesData
from tracereq.vsm import measurement
from tracereq.lsa import latentSemantic
from tracereq.lda import latentDirichlet

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
        req= myProses.fulldataset(srs_param)['Requirement Statement'] # myProses.preprocessing()
        id_req= myProses.fulldataset(srs_param)['ID']
        cleaned_text = myProses.apply_cleaning_function_to_list(list(req))
        hasil_bow = measurement().bow(req, id_req, 'english')
        hasil_tfidf = measurement().tfidf(req, id_req, 'l2', 'english')
        hasil_lsa = latentSemantic(req).ukurLSA(id_req)
        hasil_lda = latentDirichlet(req).lda_feature(id_req)
        hasil_kl = latentDirichlet(req).Kullback_feature(id_req)
        hasil_fr = latentDirichlet(req).Frobenius_norm_feature(id_req)
        
        pilihan = st.sidebar.selectbox('pilih metode?', ('bow', 'tfidf', 'frobenius', 'kullback', 'lda', 'lsa'))
        if 'bow' in pilihan:
            st.write(hasil_bow)
        if 'tfidf' in pilihan:
            st.write(hasil_tfidf)
        elif 'lsa' in pilihan:
            st.write(hasil_lsa)
        elif 'frobenius' in pilihan:
            st.write(hasil_fr)
        elif 'kullback' in pilihan:
            st.write(hasil_kl)
        elif 'lda' in pilihan:
            st.write(hasil_lda)
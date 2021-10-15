import streamlit as st, pandas as pd
from tracereq.preprocessing_evaluation import prosesData
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from tracereq.vsm import measurement
from tracereq.lsa import latentSemantic
from tracereq.lda import latentDirichlet

def bow(data_raw, id_req, stopwords_list):
    vectorizer = CountVectorizer(stop_words= stopwords_list)
    X = vectorizer.fit_transform(data_raw)
    name_fitur = vectorizer.get_feature_names()
    df = pd.DataFrame(X.toarray(), index= id_req, columns = name_fitur)
    return df

def tfidf(data_raw, id_req, norm_list, stopwords_list):
    vectorizer = TfidfVectorizer(norm= norm_list, stop_words= stopwords_list)
    X = vectorizer.fit_transform(data_raw)
    name = vectorizer.get_feature_names()
    df = pd.DataFrame(X.toarray(), index= id_req, columns= name)
    return df

def fitur_lda_lsa(data_raw, id_req, output= ['fr', 'kl', 'lda', 'lsa']):
    data_lsa = latentSemantic(data_raw).ukurLSA(id_req)
    data_fr = latentDirichlet(data_raw).Frobenius_norm_feature(id_req)
    data_kl = latentDirichlet(data_raw).Kullback_feature(id_req)
    data_lda = latentDirichlet(data_raw).lda_feature(id_req)
    if 'fr' in output:
        return data_fr
    elif 'kl' in output:
        return data_kl
    elif 'lda' in output:
        return data_lda
    elif 'lsa' in output:
        return data_lsa

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
        id_req = myProses.fulldataset(srs_param)['ID']

        norm_list = st.sidebar.selectbox('pilih normalize?', ('l2', 'l1', 'max'))
        stopwords_list = st.sidebar.selectbox('pilih stopwords?', ('english', 'indonesian'))
        data_bow = bow(data_raw, id_req, stopwords_list)
        data_tfidf = tfidf(data_raw, id_req, norm_list, stopwords_list)
        data_lsa = fitur_lda_lsa(data_raw, id_req, 'lsa')
        data_lda = fitur_lda_lsa(data_raw, id_req, 'lda')
        data_fr = fitur_lda_lsa(data_raw, id_req, 'fr')
        data_kl = fitur_lda_lsa(data_raw, id_req, 'kl')
        cs_bow = measurement(data_raw).cosine_measurement(data_bow, id_req)
        cs_tfidf = measurement(data_raw).cosine_measurement(data_tfidf, id_req)
        cs_lsa = measurement(data_raw).cosine_measurement(data_lsa, id_req)
        cs_lda = measurement(data_raw).cosine_measurement(data_lda, id_req)
        cs_fr = measurement(data_raw).cosine_measurement(data_fr, id_req)
        cs_kl = measurement(data_raw).cosine_measurement(data_kl, id_req)

        pilihan = st.sidebar.selectbox('pilih metode?', ('bow', 'tfidf', 'frobenius', 'kullback', 'lda', 'lsa'))
        if 'bow' in pilihan:
            st.write(data_bow)
            st.write(cs_bow)
        if 'tfidf' in pilihan:
            st.write(data_tfidf)
            st.write(cs_tfidf)
        elif 'lsa' in pilihan:
            st.write(data_lsa)
            st.write(cs_lsa)
        elif 'frobenius' in pilihan:
            st.write(data_fr)
            st.write(cs_fr)
        elif 'kullback' in pilihan:
            st.write(data_kl)
            st.write(cs_kl)
        elif 'lda' in pilihan:
            st.write(data_lda)
            st.write(cs_lda)
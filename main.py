import nltk
nltk.download('stopwords')

import streamlit as st
import spacy_streamlit
from extractreq.modul_ekspart import partOf, pd
from extractreq.modul_spacySent import spacyClause #, spacy#, spacy_param

st.header("Ekspart Module")
st.markdown("Modul usulan ini digunakan untuk melihat kebergantungan kebutuhan berdasarkan ekspart")

dataset1 = st.file_uploader("Choose a file", key= 'test') 
if dataset1 is not None:
     st.sidebar.header('Dataset Test Parameter')
     x1 = pd.ExcelFile(dataset1)
     srs_param = st.sidebar.selectbox( 'What Dataset you choose?', x1.sheet_names)
     part1 = partOf(dataset1) # Load data example (dari functional maupun nonfunctional)
     dataReq = part1.fulldataset(srs_param)
     data_filtrasi = part1.tabulasi_filter(dataReq)
     data_pertama = part1.tabulasi_pertama(data_filtrasi, dataReq)
     data_kedua = part1.tabulasi_kedua(data_pertama)
     data_stat = part1.nilai_stat(data_pertama, data_kedua)

     nlp = spacy_streamlit.load("en_core_web_sm")
     data_spacy = []
     for idx, num in zip(dataReq['ID'], dataReq['Requirement Statement']):
          doc = nlp(num)
          myClause = spacyClause(dataset1).extractData(doc)
          jml_data = len(myClause)
          label_df = []
          if jml_data > 1: # non atomik berdasarkan jumlah
               label_df.append('non_atomik')
          elif jml_data == 1:
               label_df.append('atomik')
          else:
               label_df.append('unknown')
          data_spacy.append([idx, myClause, label_df[0], jml_data])
     filterSpacy = pd.DataFrame(data_spacy, columns= ['ID', 'data', 'label', 'jumlah'])
     data2Spacy = part1.tabulasi_kedua(filterSpacy)
     stat_spacy = part1.nilai_stat(filterSpacy, data2Spacy)
     part1.__del__() 

     ml_mode = st.sidebar.selectbox( 'pilihan mode?', ['manual', 'spacy'])
     if 'spacy' in ml_mode:
          srs_param = st.sidebar.selectbox( 'tabulasi?', ['pertama', 'kedua', 'stat'])
          st.header('Tabel Dataset Spacy')
          if 'pertama' in srs_param:
               st.table(filterSpacy)
          elif 'kedua' in srs_param:
               st.table(data2Spacy)
          elif 'stat' in srs_param:
               st.table(stat_spacy)

     elif 'manual' in ml_mode:
          srs_param = st.sidebar.selectbox( 'tabulasi?', ['pertama', 'kedua', 'stat'])
          st.header('Tabel Dataset Manual')
          if 'pertama' in srs_param:
               st.table(data_pertama)
          elif 'kedua' in srs_param:
               st.table(data_kedua)
          elif 'stat' in srs_param:
               st.table(data_stat)

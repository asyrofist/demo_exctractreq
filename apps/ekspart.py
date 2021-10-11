import streamlit as st
from extractreq.modul_ekspart import partOf, pd
from extractreq.modul_spacySent import spacyClause, id_param, col_param
from extractreq.modul_stanfordSent import stanford_clause, id_param, col_param

def app():
    st.header("Ekspart Module")
    st.markdown("Modul usulan ini digunakan untuk melihat kebergantungan kebutuhan berdasarkan ekspart")

    dataset1 = st.file_uploader("Choose a file", key= 'ekspart') 
    if dataset1 is None:
        st.warning("masukkan data terlebih dahulu")

    elif dataset1 is not None:
        st.sidebar.header('Dataset Test Parameter')
        x1 = pd.ExcelFile(dataset1)
        srs_param = st.sidebar.selectbox( 'What Dataset you choose?', x1.sheet_names)

        part1 = partOf(dataset1) # manual data
        dataReq = part1.fulldataset(srs_param)
        part1.__del__() 

        ml_mode = st.sidebar.selectbox( 'pilihan mode?', ['manual', 'spacy', 'stanford'])
        if 'stanford' in ml_mode:
            st.header('Tabel Dataset Stanford')
            data_pertama = stanford_clause(dataset1).main(srs_param, id_param, col_param) # spacy
        if 'spacy' in ml_mode:
            st.header('Tabel Dataset Spacy')
            data_pertama = spacyClause(dataset1).main(srs_param, id_param, col_param) # spacy
        elif 'manual' in ml_mode:
            st.header('Tabel Dataset Manual')
            data_filtrasi = part1.tabulasi_filter(dataReq)
            data_pertama = part1.tabulasi_pertama(data_filtrasi, dataReq)

        data_kedua = part1.tabulasi_kedua(data_pertama)
        data_stat = part1.nilai_stat(data_pertama, data_kedua)
        srs_param = st.sidebar.selectbox( 'tabulasi?', ['pertama', 'kedua', 'stat'])
        if 'pertama' in srs_param:
            st.table(data_pertama)
            st.success("succes load")
        elif 'kedua' in srs_param:
            st.table(data_kedua)
            st.success("succes load")
        elif 'stat' in srs_param:
            st.table(data_stat)
            st.success("succes load")

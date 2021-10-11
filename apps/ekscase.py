import nltk
nltk.download('stopwords')

import streamlit as st
from extractreq.usecase_modul1 import xmlParser, pd
from extractreq.usecase_modul2 import parsingRequirement
from extractreq.usecase_modul3 import ucdReq
from pywsd.cosine import cosine_similarity

def useCaseMeasurement(keyword1, keyword2, id1, id2):
     hasil_wsd = [[cosine_similarity(num, angka) for angka in keyword2] for num in keyword1]
     df = pd.DataFrame(hasil_wsd, index= id1, columns= id2)
     return df

def app():
    st.header("Ekscase Module")
    st.markdown("Modul usulan ini digunakan untuk melihat kebergantungan kebutuhan berdasarkan ekspart")

    metode = st.sidebar.selectbox( 'modul?', ['xmlparser', 'parsingreq', 'ucdreq'])
    if 'ucdreq' in metode:
        st.header("Modul 3")
        st.markdown("Modul usulan ini digunakan untuk melihat relasi include dan extend pada usecase")
        dataset1 = st.sidebar.file_uploader("Choose a file", key= 'aksi_aktor') 
        dataset2 = st.sidebar.file_uploader("Choose a file", key= 'data_xmi') 
        if dataset1 and dataset2 is not None:
            MyucdReq = ucdReq(dataset1, dataset2)
            freqs = MyucdReq.fulldataset('tabel_freqs')# data dari txt
            ucd1 = MyucdReq.fulldataset('tabel_ucd1') # data dari txt
            ucd2 = MyucdReq.fulldataset('tabel_ucd2') # data dari txt
            useCaseTable  = MyucdReq.fulldataset_xmi('tabel_usecase') # dari xmi

            tbl_1 = MyucdReq.ucdMeasurement(freqs.aksi, ucd1.dropna().aksi)
#             tbl_1.columns = ucd1.dropna().usecase # kalkulasi tabel 1
            tbl_1.index = freqs.id

            tbl_2 = MyucdReq.ucdMeasurement(freqs.aksi, ucd2.dropna().aksi)
#             tbl_2.columns = ucd2.dropna().usecase # kalkulasi tabel 2
            tbl_2.index = freqs.id

            data_ucd = [MyucdReq.change_case(num) for num in useCaseTable.name]
            tbl_1x = MyucdReq.ucdMeasurement(freqs.aksi, data_ucd)
            tbl_1x.index = freqs.id # kalkulasi tabel 3
#             tbl_1x.columns = useCaseTable.name

            tbl_4 = useCaseMeasurement(freqs.aksi, ucd1.dropna().aksi, freqs.id, ucd1.dropna().usecase)
            tbl_5 = useCaseMeasurement(freqs.aksi, ucd2.dropna().aksi, freqs.id, ucd2.dropna().usecase)
            tbl_6 = useCaseMeasurement(freqs.aksi, data_ucd, freqs.id, useCaseTable.name)

        elif dataset1 is None:
            st.warning("masukkan data aksi_aktor.xlsx terlebih dahulu..")

        elif dataset2 is None:
            st.warning("masukkan data xmi.xslsx juga..")

        tabulasi_ucdreq = st.selectbox( 'pilihan tabel?', ['pertama', 'kedua', 'ketiga', 'keempat', 
        'tabel1', 'tabel2', 'tabel3', 'tabel4', 'table5', 'table6'])
        if 'pertama' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
            st.table(freqs)
        elif 'kedua' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
            st.table(ucd1)
        elif 'ketiga' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
            st.table(ucd2)
        elif 'keempat' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
            st.table(useCaseTable)
        elif 'tabel1' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
            st.table(tbl_1)
        elif 'tabel2' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
            st.table(tbl_2)
        elif 'tabel3' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
            st.table(tbl_1x)
        elif 'tabel4' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
            st.table(tbl_4)
        elif 'tabel5' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
            st.table(tbl_5)
        elif 'tabel6' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
            st.table(tbl_6)
        else:
            st.warning("masukkan data terlebih dahulu")


    if 'parsingreq' in metode:
        st.header("Modul 2")
        st.markdown("Modul usulan ini mengekstraksi data usecase dari dokumen txt")
        dataset1 = st.sidebar.file_uploader("Choose a file", key= 'freqs') 
        if dataset1 is not None:
            MyParsingRequirement = parsingRequirement(dataset1)
            freqs = MyParsingRequirement.membacaCSV()
            data_freqs = MyParsingRequirement.data_raw(freqs.requirement)
            cleaned_freq = MyParsingRequirement.apply_cleaning_function_to_list(data_freqs)
            freqs['aksi'] = [MyParsingRequirement.aksi_aktor(num)[1] for num in cleaned_freq]
            freqs['aktor'] = [MyParsingRequirement.aksi_aktor(num)[0] for num in cleaned_freq]

        elif dataset1 is None:
            st.sidebar.warning("masukkan data freqs.txt terlebih dahulu")

            # parsing ucd1
        dataset2 = st.sidebar.file_uploader("Choose a file", key= 'ucd1') 
        if dataset2 is not None:
            MyParsingRequirement = parsingRequirement(dataset2)
            ucd1 = MyParsingRequirement.membacaCSV()
            data_ucd1 = MyParsingRequirement.data_raw(ucd1.flowOfEvents)
            list_index= [("data{}".format(idx)) for idx, num in enumerate(data_ucd1)]
            data_list = pd.DataFrame(data_ucd1, index= list_index)
            data_list = data_list.drop(index= "data5").reset_index().drop(labels= ['index'], axis= 1)
            ucd1['aksi'] = data_list
            cleaned1_ucd = MyParsingRequirement.apply_cleaning_function_to_list(list(ucd1.aksi))
            ucd1['aksi'] = [MyParsingRequirement.aksi_aktor(num)[1] for num in cleaned1_ucd]
            ucd1['aktor'] = [MyParsingRequirement.aksi_aktor(num)[0] for num in cleaned1_ucd]

        elif dataset2 is None:
            st.sidebar.warning("masukkan data ucd1.txt terlebih dahulu")

            # parsing ucd2
        dataset3 = st.sidebar.file_uploader("Choose a file", key= 'ucd2') 
        if dataset3 is not None:
            MyParsingRequirement = parsingRequirement(dataset3)
            ucd2 = MyParsingRequirement.membacaCSV()
            data_ucd2 = MyParsingRequirement.data_raw(ucd2.flowOfEvents)
            list2_index= [("data{}".format(idx)) for idx, num in enumerate(data_ucd2)]
            data2_list = pd.DataFrame(data_ucd2, index= list2_index)
            data2_list = data2_list.reset_index().drop(labels= ['index'], axis= 1)
            ucd2['aksi'] = data2_list
            cleaned2_ucd = MyParsingRequirement.apply_cleaning_function_to_list(list(ucd2.aksi))
            ucd2['aksi'] = [MyParsingRequirement.aksi_aktor(num)[1] for num in cleaned2_ucd]
            ucd2['aktor'] = [MyParsingRequirement.aksi_aktor(num)[0] for num in cleaned2_ucd]

        elif dataset3 is None:
            st.sidebar.warning("masukkan data ucd2.txt terlebih dahulu")

        tabulasi_parse = st.selectbox( 'pilihan xml?', ['freqs', 'ucd1', 'ucd2'])
        if 'freqs' in tabulasi_parse and dataset1 is not None:
            st.table(freqs)
            st.success("succes load")
        elif 'ucd1' in tabulasi_parse and dataset2 is not None:
            st.table(ucd1)
            st.success("succes load")
        elif 'ucd2' in tabulasi_parse and dataset3 is not None:
            st.table(ucd2)
            st.success("succes load")
        else:
            st.warning("masukkan data terlebih dahulu")

    elif 'xmlparser' in metode:
        st.header("Modul 1")
        st.markdown("Modul usulan ini mengekstraksi data usecase dari dokumen xmi")
        dataset = st.file_uploader("Choose a file", key= 'xmlparser') 
        if dataset is None:
            st.warning("masukkan data terlebih dahulu")

        elif dataset is not None:
            paketElemen = xmlParser(dataset).dataPaketElemen()
            tabulasi_xml = st.sidebar.selectbox( 'pilihan xml?', ['daftarActor', 'daftarUsecase'])
            actorTable = paketElemen[paketElemen['type'] == 'uml:Actor']
            useCaseTable = paketElemen[paketElemen['type'] == 'uml:UseCase']
            if 'daftarActor' in tabulasi_xml:
                st.table(actorTable)
                st.success("succes load")
            elif 'daftarUsecase' in tabulasi_xml:
                st.table(useCaseTable)
                st.success("succes load")

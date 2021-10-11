from google.protobuf.descriptor import MethodDescriptor
import nltk
nltk.download('stopwords')

import streamlit as st
from extractreq.modul_ekspart import partOf, pd
from extractreq.modul_spacySent import spacyClause, id_param, col_param
from extractreq.modul_stanfordSent import stanford_clause, id_param, col_param
from extractreq.usecase_modul1 import xmlParser
from extractreq.usecase_modul2 import parsingRequirement
from extractreq.usecase_modul3 import ucdReq

metode = st.selectbox( 'Apa pilihan modul anda?', ['ekspart', 'ekscase'])
if 'ekscase' in metode:
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

          elif dataset1 is None:
               st.warning("masukkan data aksi_aktor.xlsx terlebih dahulu..")

          elif dataset2 is None:
               st.warning("masukkan data xmi.xslsx juga..")

          tabulasi_ucdreq = st.selectbox( 'pilihan tabel?', ['pertama', 'kedua', 'ketiga', 'keempat'])
          if 'pertama' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
               st.table(freqs)
          elif 'kedua' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
               st.table(ucd1)
          elif 'ketiga' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
               st.table(ucd2)
          elif 'keempat' in tabulasi_ucdreq and dataset1 and dataset2 is not None:
               st.table(useCaseTable)
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

elif 'ekspart' in metode:
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


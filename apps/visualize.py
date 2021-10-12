import streamlit as st, pandas_profiling 
from streamlit_pandas_profiling import st_profile_report
from extractreq.modul_ekspart import partOf, pd

def app():
    st.header("Visualize Statistic Module")
    st.markdown("Modul ini digunakan untuk mengolah data secara statistik")

    dataset1 = st.file_uploader("Choose a file", key= 'ekspart') 
    if dataset1 is None:
        st.warning("masukkan data terlebih dahulu")

    elif dataset1 is not None:
        st.sidebar.header('Dataset Pandas Profiling')
        x1 = pd.ExcelFile(dataset1)
        srs_param = st.sidebar.selectbox( 'What Dataset you choose?', x1.sheet_names)
        part1 = partOf(dataset1) # manual data
        df = part1.fulldataset(srs_param)
        st.table(df)
        pr = df.profile_report()
        st_profile_report(pr)

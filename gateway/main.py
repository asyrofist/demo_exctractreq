import json, streamlit as st, requests, pandas as pd

option = st.sidebar.selectbox('API?', ('cat_breeds', 'cat_facts', 'dog', 'country', 'random', 'penguinrandom'))
if 'cat_facts' in option:
    st.title("CAT Facts")
    urlData = "https://cat-fact.herokuapp.com/facts"
    data = requests.get(urlData) # merequest urldata 
    json_data = json.loads(data.content) # meload json_data
    a = pd.DataFrame.from_dict(json_data) # membuat tabel dari json_data
    data_list = [num for num in a['status']] # membuat data_list
    list_df = pd.DataFrame(data_list) # membuat dataframe list_df
    df = pd.concat([a, list_df], axis= 1) #menggabungkan list_df dan a
    options = st.sidebar.multiselect('drop columns?',[df.columns][0],
    ['status', 'sentCount', 'deleted', '__v', 'used', 'verified'])
    st.write(df.drop(options, axis=1)) # menghapus status

elif 'cat_breeds' in option:
    st.title("CAT Breeds")
    urlData = "https://api.thecatapi.com/v1/breeds"
    data = requests.get(urlData) # merequest urldata 
    json_data = json.loads(data.content) # meload json_data
    list_source = pd.DataFrame.from_dict(json_data) # membuat tabel dari json_data
    list_filter = list_source.dropna(axis= 1)
    options = st.sidebar.multiselect('drop columns?',[list_filter.columns][0],
    ['weight', 'country_code'])
    st.write(list_filter.drop(options, axis= 1))

elif 'dog' in option:
    st.title("Dog")
    pilihanUrl = st.sidebar.selectbox('pilihAPI?', 
    ("url1","url2", 'url3'))
    if "url1" in pilihanUrl:
        urlData = "https://dog.ceo/api/breeds/list/all"
    elif "url2" in pilihanUrl:
        urlData = "https://dog.ceo/api/breed/hound/images"
    elif "url3" in pilihanUrl:
        urlData = "https://dog.ceo/api/breed/hound/list"

    data = requests.get(urlData) # merequest urldata 
    json_data = json.loads(data.content) # meload json_data
    list_source = pd.DataFrame.from_dict(json_data) # membuat tabel dari json_data
    st.write(list_source)

elif 'country' in option:
    st.title("Country")
    pilihanUrl = st.sidebar.selectbox('pilihAPI?', 
    ("url1", "url2", 'url3', 'url4'))
    if "url1" in pilihanUrl:
        urlData = "http://apiv3.iucnredlist.org/api/v3/country/list?token=9bb4facb6d23f48efbf424bb05c0c1ef1cf6f468393bc745d42179ac4aca5fee"
    elif "url2" in pilihanUrl:
        urlData = "http://apiv3.iucnredlist.org/api/v3/region/list?token=9bb4facb6d23f48efbf424bb05c0c1ef1cf6f468393bc745d42179ac4aca5fee"
    elif "url3" in pilihanUrl:
        urlData = "http://apiv3.iucnredlist.org/api/v3/species/page/0?token=9bb4facb6d23f48efbf424bb05c0c1ef1cf6f468393bc745d42179ac4aca5fee"
    elif "url4" in pilihanUrl:
        urlData = "http://apiv3.iucnredlist.org/api/v3/species/region/europe/page/0?token=9bb4facb6d23f48efbf424bb05c0c1ef1cf6f468393bc745d42179ac4aca5fee"
    data = requests.get(urlData) # merequest urldata 
    json_data = json.loads(data.content) # meload json_data
    list_source = pd.DataFrame.from_dict(json_data) # membuat tabel dari json_data
    st.write(list_source)

elif 'random' in option:
    st.title("Random PETS")
    pilihanUrl = st.sidebar.selectbox('pilihAPI?', 
    ("url1", "url2", 'url3'))
    if "url1" in pilihanUrl:
        urlData = "https://aws.random.cat/meow"
    elif "url2" in pilihanUrl:
        urlData = "https://random.dog/woof.json"
    elif "url3" in pilihanUrl:
        urlData = "https://randomfox.ca/floof/"
    data = requests.get(urlData) # merequest urldata 
    json_data = json.loads(data.content) # meload json_data
    st.write(json_data)

elif 'penguinrandom' in option:
    st.title("Random PETS")
    urlData = "http://www.penguinrandomhouse.biz/resources/works"
    data = requests.get(urlData) # merequest urldata 
    json_data = json.loads(data.content) # meload json_data
    st.write(json_data)
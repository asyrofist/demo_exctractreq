import json, requests, pandas as pd, streamlit as st

backend = "http://localhost:8000/register"

st.title("Halo ini sekedar test")
ok = requests.get(backend)
# data_json = ok.json()

data_json = json.loads(ok.content)
st.table(data_json)

# df = pd.read_json(backend)
# st.write(df)
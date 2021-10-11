import nltk
nltk.download('stopwords')

import streamlit as st
from google.protobuf.descriptor import MethodDescriptor
from apps.multiapp import MultiApp
from apps import ekscase, ekspart # import your app modules here

app = MultiApp()
app.add_app("ekspart", ekspart.app) # Add all your application here
app.add_app("ekscase", ekscase.app)
app.run() # The main app
app.__del__()

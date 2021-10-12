import nltk
nltk.download('stopwords')

import streamlit as st
from google.protobuf.descriptor import MethodDescriptor
from apps.multiapp import MultiApp
from apps import ekscase, ekspart, visualize # import your app modules here

app = MultiApp()
app.add_app("ekspart_module", ekspart.app) # Add all your application here
app.add_app("ekscase_modeul", ekscase.app)
app.add_app("visualize", visualize.app)
app.run() # The main app

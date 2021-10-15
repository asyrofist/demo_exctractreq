import nltk
nltk.download('stopwords')

import streamlit as st
from google.protobuf.descriptor import MethodDescriptor
from apps.multiapp import MultiApp
from apps import ekscase, ekspart, visualize, traceability # import your app modules here

app = MultiApp()
app.add_app("ekspart_module", ekspart.app) # Add all your application here
app.add_app("ekscase_module", ekscase.app)
app.add_app("visualize_module", visualize.app)
app.add_app("tracereq_module", traceability.app)
app.run() # The main app

import streamlit as st, nltk
from google.protobuf.descriptor import MethodDescriptor
from apps.multiapp import MultiApp
from apps import ekscase, ekspart # import your app modules here

nltk.download('stopwords')
app = MultiApp()

# Add all your application here
app.add_app("ekspart", ekspart.app)
app.add_app("ekscase", ekscase.app)

# The main app
app.run()

import streamlit as st
from google.protobuf.descriptor import MethodDescriptor
from apps.multiapp import MultiApp
from apps import ekscase, ekspart # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("ekspart", ekspart.app)
app.add_app("ekscase", ekscase.app)

# The main app
app.run()

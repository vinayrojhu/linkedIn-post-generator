from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

from pydantic.v1.schema import model_type_schema
import streamlit as st

# Use secrets in production, .env in local
if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
else:
    api_key = st.secrets["GROQ_API_KEY"]

llm = ChatGroq(groq_api_key=api_key, model_name = "llama-3.3-70b-versatile")

if __name__ == "__main__" :
    response = llm.invoke("what is main ingridients in samosa ")
    print(response.content)

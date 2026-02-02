import os
from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

# --------------------------------------------------
# LOAD .env FROM SAME DIRECTORY AS main.py
# --------------------------------------------------
env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)

# DEBUG (optional – remove later)
#st.write("DEBUG ENV PATH:", env_path)
#st.write("DEBUG API KEY:", os.getenv("OPEN_API_KEY"))

if not os.getenv("OPEN_API_KEY"):
    st.error("OPEN_API_KEY not found. Please check your .env file.")
    st.stop()

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    url_input = st.text_input(
        "Enter a URL:",
        value="https://jobs.nike.com/job/R-33460"
    )

    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            for job in jobs:
                skills = job.get("skills", [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language="markdown")

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        page_title="Cold Email Generator",
        page_icon="📧"
    )

    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)

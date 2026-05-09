import io, traceback, warnings

from dotenv import load_dotenv
import os

import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent

warnings.filterwarnings("ignore")
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL = "llama-3.3-70b-versatile"
print("KEY:", os.getenv("GROQ_API_KEY"), GROQ_API_KEY)

st.set_page_config(page_title="DataMind", page_icon="🧠", layout="centered")
st.title("🧠 DataMind")
st.caption("AI-агент для анализа данных | Groq + LangChain")

uploaded = st.file_uploader("Загрузить датасет", type=["csv", "xlsx", "xls"])

if uploaded:
    try:
        df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
        st.session_state.df = df
    except Exception as e:
        st.error(f"Ошибка загрузки: {e}")
        st.stop()

if "df" not in st.session_state:
    st.stop()

df = st.session_state.df
st.success(f"Загружен датасет: {df.shape[0]:,} строк x {df.shape[1]} столбцов")

@st.cache_resource(show_spinner=False)
def get_agent(_df):
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name=MODEL, temperature=0)
    return create_pandas_dataframe_agent(
            llm,
            _df,
            agent_type="openai-tools",
            allow_dangerous_code=True,  
            early_stopping_method="generate", 
            max_iterations=10,  
            handle_parsing_errors=True,
        )

agent = get_agent(df)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        for img in msg.get("images", []):
            img.seek(0)
            st.image(img, use_container_width=True)

user_input = st.chat_input("Задай вопрос по датасету...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Анализирую..."):
            plt.close("all")
            try:
                result = agent.invoke({"input": user_input})
                answer = result.get("output", str(result))
            except Exception as e:
                answer = traceback.format_exc()

            images = []
            for n in plt.get_fignums():
                b = io.BytesIO()
                plt.figure(n).savefig(b, format="png", dpi=130, bbox_inches="tight")
                b.seek(0)
                images.append(b)
            plt.close("all")

            st.markdown(answer)
            for img in images:
                img.seek(0)
                st.image(img, use_container_width=True)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "images": images,
            })

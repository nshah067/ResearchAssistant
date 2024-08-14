import streamlit as st
from modules import *
from utils import download_pdf

urls = [
    "",
    "",
    "",
]

papers = [
    "timegpt",
    "moment",
    "ttm",
]

st.title("AI Powered Research Assistant")
s = True
with st.form("Research Materials"):
    st.write("To start, enter 3 research papers along with a url.  \nWhen you are done, press 'Retrieve Materials'")
    i1 = st.text_input("Format: [paper name, paper url]", value="timegpt, https://arxiv.org/pdf/2310.03589").split(",")
    i2 = st.text_input("Format: [paper name, paper url]", value="moment, https://arxiv.org/pdf/2402.03885").split(",")
    i3 = st.text_input("Format: [paper name, paper url]", value="ttm, https://arxiv.org/pdf/2401.03955",).split(",")
    s = st.form_submit_button("Retrieve Materials")
    if s:
        papers[0], urls[0] = i1[0], i1[1]
        papers[1], urls[1] = i2[0], i2[1]
        papers[2], urls[2] = i3[0], i3[1]
        for url, paper in zip(urls, papers):
            download_pdf(url, paper)
id = 0
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Start Chatting", key=f"{id}"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        output = manydocAgent(papers).chat(prompt)
        reply = str(output.response)
        sources = output.source_nodes
        citation = ""
        for i in range(min(len(sources), 3)):
            source = sources[i]
            num = i + 1
            citation += f"{num}: Page {source.metadata['page_label']} in {source.metadata['file_name']}  \n"
        reply = reply.replace("assistant: ", "")
        response = f"{reply}  \nSources:  \n{citation}  \n"
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
import re
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.chains.question_answering import load_qa_chain
import streamlit as st
import os

from langchain.vectorstores import FAISS
load_dotenv()

st.set_page_config(page_title="Conversaltional ChatBot", layout="wide")
st.header("Ask me anything")

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
    task="text-generation",
    model_kwargs={"token": os.environ["HUGGINGFACEHUB_API_TOKEN"]},
    max_new_tokens=200,
    temperature=0.6,
    do_sample=False,
)

system_prompt = """
  Anser the question politely and in a professional manner from the following data, reply as a subordinate to the company in the context.
  If Question is unrelated to following text reply with "I don't know".
  data:\n {context}\n
  Question:\n{question}\n

  answer:

  """
prompt = PromptTemplate(
      input_variables=["context", "question"],
      template=system_prompt
  )

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, how can I help you?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def ensure_complete_sentence(text):
    # Find the last sentence-ending punctuation mark
    match = re.search(r'([.!?])([^.!?]*)$', text)
    if match:
        end_idx = match.end(1)
        return text[:end_idx + 1]
    else:
        return text

def get_response(question):
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.load_local("./faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = db.similarity_search(question)
    chain = load_qa_chain(llm=llm, chain_type="stuff")
    output = chain.run(input_documents=docs, question=question)

    return output

input = st.chat_input("Write your query here")

if input is not None:
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.write(input)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            response = get_response(input)
            response = ensure_complete_sentence(response)
            st.write(response)
    new_ai_message = {"role": "assistant", "content": response}
    st.session_state.messages.append(new_ai_message)
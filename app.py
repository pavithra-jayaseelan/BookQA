import streamlit as st
from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext,SummaryIndex
from llama_index.node_parser import SentenceSplitter
from llama_index.llms import OpenAI
from llama_index.embeddings import OpenAIEmbedding
from llama_index.storage import StorageContext

api_key = "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"

if not "bot" in st.session_state:

    st.session_state.bot = ""

    loader =SimpleDirectoryReader("books")

    docs = loader.load_data()

    llm = OpenAI(api_key=api_key)

    embeddings = OpenAIEmbedding(api_key=api_key)

    service_context = ServiceContext.from_defaults(llm=llm,embed_model=embeddings)

    node_parser = SentenceSplitter(chunk_size=1200)

    nodes = node_parser.get_nodes_from_documents(docs)

    index = VectorStoreIndex(nodes=nodes,service_context=service_context)

    index.storage_context.persist("QA_BOT")

    engine = index.as_chat_engine()

    if not st.session_state.bot:

        st.session_state.bot = engine

st.title("Book Question and Answering.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = st.session_state.bot.chat(prompt).response

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


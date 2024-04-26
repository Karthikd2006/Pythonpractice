#pip install langchain_community tiktoken langchain-openai langchainhub chromadb langchain

import os
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = 'ls__307693ebd0cb42a1abdfc9363534cb27'

os.environ['OPENAI_API_KEY'] = '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'

import bs4
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

#### INDEXING ####

# Load Documents

# loader = WebBaseLoader(
#     web_paths=("https://isha.sadhguru.org/en/center/consecrated-spaces/112-feet-adiyogi",),
#     bs_kwargs=dict(
#         parse_only=bs4.SoupStrainer(
#             class_=("css-10ngtyv")
#         )
#     ),
# )
# docs = loader.load()

# #print(docs)

# # Split
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(docs)

# Embed
#embeddingFunction = SentenceTransformerEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#vectorstore = chroma.Chroma.from_documents(documents=splits, embedding=embeddingFunction)

persistDirectory = "C:/karthik/RFP/vectordb"

#vectorstore = chroma.Chroma.from_documents(documents=splits, persist_directory= persistDirectory,
#                                    embedding=OpenAIEmbeddings())

vectorstore = chroma.Chroma(persist_directory= persistDirectory,
                                    embedding_function=OpenAIEmbeddings())

retriever = vectorstore.as_retriever()

#### RETRIEVAL and GENERATION ####

#Prompt
prompt = hub.pull("rlm/rag-prompt")

# LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Question
answerResponse = rag_chain.invoke("What is the source of yoga?")

print(answerResponse)


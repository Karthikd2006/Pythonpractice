#pip install langchain_community tiktoken langchain-openai langchainhub chromadb langchain

import os
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = 'ls__307693ebd0cb42a1abdfc9363534cb27'

os.environ['OPENAI_API_KEY'] = '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'

import bs4
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
#from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.document_loaders import PyPDFLoader
#from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


#### INDEXING ####

# Load Documents

#loader = PyPDFLoader("C:/karthik/RFP/gre.pdf")

loader = PyPDFLoader("https://www.indiabudget.gov.in/doc/bh1.pdf", extract_images=True)
pages = loader.load()

print(pages[0].page_content)

#Split
#text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#splits = text_splitter.split_documents(pages)

#Embed

# faiss_index = FAISS.from_documents(pages, OpenAIEmbeddings())
# docs = faiss_index.similarity_search("Who is the producer of this pdf?", k=2)
# for doc in docs:
#     print(str(doc.metadata["page"]) + ":", doc)

# ### RETRIEVAL and GENERATION ####

# #Prompt
# prompt = hub.pull("rlm/rag-prompt")

# # LLM
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# # Post-processing
# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

# # Chain
# rag_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )

# # Question
# answerResponse = rag_chain.invoke("Who is the producer of this pdf?")

# print(answerResponse)


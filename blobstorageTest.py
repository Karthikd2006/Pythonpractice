#pip install azure-storage-blob

#from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

import os
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = 'ls__307693ebd0cb42a1abdfc9363534cb27'

os.environ['OPENAI_API_KEY'] = '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'

import bs4
from langchain import hub
from azure.storage.blob import BlobServiceClient
from langchain_community.vectorstores import chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

# Connect to Blob Storage
connection_string = "DefaultEndpointsProtocol=https;AccountName=sampleembedding;AccountKey=IAnnCO2GNsCJongOBovsvhHfjY/bs6hm5JN40glNJ+KaR4iZ92YR0J/jd0DNwKc6hW3+sZF7DTy++AStZ9mfiQ==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

def persist_directory(directory_name, data=None):

    dirName = directory_name
    containerName = dirName.split('/')
    print(containerName)

    container_client = blob_service_client.get_container_client(containerName[0])
    
    # Check if directory exists, if not create it
    #if not container_client.exists():
    #    container_client.create_container()

    if data is None:
        # Read files from blob storage
        blob_list = container_client.list_blobs(name_starts_with=containerName[1])
        files = {}
        for blob in blob_list:
            blob_client = container_client.get_blob_client(blob)
            # Assuming each blob corresponds to a file, you can adjust this part according to your blob naming convention
            # file_name = blob.name
            file_name = blob.name.split('/')[-1]
            print("File_name:", file_name)
            content = blob_client.download_blob().readall()
            files[file_name] = content

            #if "chroma.sqlite3" in files:
            with open("chroma.sqlite3", "wb") as file:
                file.write(files["chroma.sqlite3"])

            chroma_file_path = os.getcwd()
            
        return chroma_file_path
    #else:
     #   # Write files to blob storage
     #   for file_name, content in data.items():
     #       blob_client = container_client.get_blob_client(file_name)
     #       blob_client.upload_blob(content)

# Embed
embeddingFunction = SentenceTransformerEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = chroma.Chroma(persist_directory= persist_directory("x-company-y-product/y-product123"),
                                    embedding_function=embeddingFunction)

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

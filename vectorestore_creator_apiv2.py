import os
from fastapi import FastAPI
from azure.storage.blob import BlobServiceClient
from langchain_community.document_loaders import PDFMinerLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import chroma
from starlette.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# It's better to use environment variables for sensitive data
connect_str = "DefaultEndpointsProtocol=https;AccountName=quickbidaicusdocuments;AccountKey=jzNsv7iojdJrGTJ6xnNzPNU7T5+/iodRPWH8bUjgId0OVtIG/oiC60n9vs5fRlZsIkOxfW4xO+tw+ASt+SFVLw==;EndpointSuffix=core.windows.net"

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

class Datastore(BaseModel):
    datastore_name: str

@app.post("/create-vector-store/")
async def create_vector_store(datastore: Datastore):
    datastore_name = datastore.datastore_name
    container_client = blob_service_client.get_container_client(datastore_name)
    docsFolder = "docs/"
    blob_list = container_client.list_blobs(name_starts_with=docsFolder)
    print("blob_list", blob_list)
    local_directory_path = f"./data/{datastore_name}/"

    if not os.path.exists(local_directory_path):
        os.makedirs(local_directory_path)

    # Download files
    for blob in blob_list:
        print(blob.name)
        if blob.name.endswith('/'):
            continue  # Skip directories
        blob_client = blob_service_client.get_blob_client(container=datastore_name, blob=blob.name)
        download_file_path = os.path.join(local_directory_path, blob.name)
        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

    # Process files
    #process_files(local_directory_path)

    # Upload the vector store
    # vector_store_path = f"./chromastore/{datastore_name}_docs"
    # upload_vector_store(datastore_name, vector_store_path)

    return JSONResponse(content={"message": "Vector store created and uploaded successfully."})

def process_files(root_directory_path):
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    print("root_directory_path:", root_directory_path)

    for root, dirs, files in os.walk(root_directory_path):
        print("root:", root)
        #if root == root_directory_path:
        #    continue

        directory_name = root.split('/')
        directory_name = directory_name[2]
        print(directory_name)
        #directory_name = os.path.basename(root)
        #persist_dir = os.path.join("./chromastore/", f"{directory_name}_RFP")
        persist_dir = os.path.join("./chromastore/", directory_name+"_docs")
        if not os.path.exists(persist_dir):
            os.makedirs(persist_dir)

        print("directory_name", directory_name)
        print("persist_dir", persist_dir)

        for file_type, loader_class in [('.pdf', PDFMinerLoader), ('.docx', Docx2txtLoader), ('.txt', TextLoader)]:
            for file in files:
                if file.endswith(file_type):
                    loader = loader_class(os.path.join(root, file))
                    doc = loader.load()
                    chunks = text_splitter.split_documents(doc)
                    clean_chunks = clean_chunk(chunks)

                    chroma.Chroma.from_documents(documents=clean_chunks, embedding=embeddings, persist_directory=persist_dir)
                    print(f"Processed and stored {file_type} files in {directory_name}")

def clean_chunk(chunks):
    for chunk in chunks:
        chunk.page_content = chunk.page_content.replace('\u200b', '')
    return chunks

def upload_vector_store(datastore_name, vector_store_path):
    
    #datastore_name = datastore_name+"vectorstore"
    container_name = datastore_name
    container_client = blob_service_client.get_container_client(container_name)
    print("container_name", container_name)
    print("container_client", container_client)

    # Create a blob with a forward slash at the end to represent a folder
    #folder_blob_name = "vectorstore/"
    #blob_client = container_client.get_blob_client(folder_blob_name)
    
    # Upload an empty blob to represent the folder
    #blob_client.upload_blob('', overwrite=True)

    # if not container_client.exists():
    #     try:
    #         print("Inside try")
    #         container_client.create_container()
    #         print(f"Container '{container_name}' created.")
    #     except Exception as e:
    #         raise Exception(f"Failed to create container '{container_name}': {e}")
    # else:
    #     print(f"Container '{container_name}' already exists.")

    print("vector_store_path", vector_store_path)

    embedding_folder = "vectorstore"  # This is used as a prefix in blob names
    for root, dirs, files in os.walk(vector_store_path):
        for file in files:
            file_path = os.path.join(root, file)
            print("file_path: " , file_path)
            blob_name = f"{embedding_folder}/{file}"
            blob_client = container_client.get_blob_client(blob=blob_name)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
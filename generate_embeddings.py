from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import JSONLoader
import os
import json
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def get_json_files_path():
    current_directory = os.getcwd()
    json_files_updated_path = os.path.join(current_directory, 'json_files_updated')
    return json_files_updated_path

if __name__ == "__main__":
    json_files_updated_path = get_json_files_path()


# Custom function to extract metadata
def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["TitleNumber"] = record.get("TitleNumber")
    metadata["TitleName"] = record.get("TitleName")
    
    chapter_list = record.get("ChapterList", [])
    hrefs = []
    for chapter in chapter_list:
        metadata['ChapterNum'] = chapter.get('ChapterNum')
        metadata['ChapterName'] = chapter.get('ChapterName')
        metadata['ArticleNum'] = chapter.get('ArticleNum')
        metadata['ArticleName'] = chapter.get('ArticleName')
        metadata['SectionNumber'] = chapter.get('SectionNumber')
        metadata['SectionTitle'] = chapter.get('SectionTitle')
        
        # Extract href from Body if available
        body_content = chapter.get("Body", "")
        soup = BeautifulSoup(body_content, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            hrefs.append(link['href'])
    
    # Combine all hrefs into a single list
    metadata['Hrefs'] = hrefs
    
    # Extract all 'Body' contents
    body_contents = [chapter.get("Body", "") for chapter in chapter_list]
    
    return {
        "metadata": metadata,
        "page_content": "\n".join(body_contents)
    }

# Instantiate loader
loader = DirectoryLoader(
    json_files_updated_path,
    glob='*.json',
    loader_cls=JSONLoader,
    loader_kwargs={
        'jq_schema': '.', 
        'content_key': None,
        'metadata_func': metadata_func,
        'text_content': False
    }
)

# Load documents directly
documents = loader.load()

# Separate the metadata from the page_content
for doc in documents:
    doc.page_content = doc.metadata['page_content']
    del doc.metadata['page_content']  

# Function to flatten metadata
def flatten_metadata(document):
    flattened_metadata = document.metadata['metadata']
    return Document(page_content=document.page_content, metadata=flattened_metadata)

# Flatten the metadata in all documents
documents = [flatten_metadata(doc) for doc in documents]

# Chunk data 
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=300)
all_splits = text_splitter.split_documents(documents)

# Instantiate embedding model 
model_name = "multi-qa-mpnet-base-dot-v1"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
hf = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# Instantiate vector db
# Create the file path to the 'embeddings' folder
persist_directory = os.path.join(current_directory, 'embeddings')

# Create the vector store and specify the persist directory
vectorstore = Chroma(persist_directory=persist_directory, embedding_function=hf)

# Generate embeddings and store in persist directory 
vectorstore = Chroma.from_documents(documents=all_splits, embedding=hf, persist_directory=persist_directory)


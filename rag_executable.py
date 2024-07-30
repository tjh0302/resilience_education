#!/usr/bin/env python
# coding: utf-8

#Minimum Reproducible Code
#RAGsilience

from ragsilience.setup_rag import create_rag_session
import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning

# Ignore specific deprecation warnings
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

# Create a session
session_id = "testing2"
embeddings_path = "/Users/zsk4gm/Desktop/resilience_education/embeddings"

rag_session = create_rag_session(session_id, embeddings_path)

def user_asks():         
    # Ask questions interactively
    while True:
        response = rag_session.ask()
        print(response)

if __name__ == '__main__': 
    user_asks()


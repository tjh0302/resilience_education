#!/usr/bin/env python
# coding: utf-8


import pytest
from ragsilience.setup_rag import OllamaSingleton, VectorstoreSingleton
from ragsilience.setup_rag import create_rag_chain
from ragsilience.setup_rag import RAGSession
import tempfile


def test_ollama_singleton():
    instance1 = OllamaSingleton.get_instance()
    instance2 = OllamaSingleton.get_instance()
    assert instance1 is instance2

def test_vectorstore_singleton():
    # Use a temporary directory for the persist_directory
    with tempfile.TemporaryDirectory() as persist_directory:
        instance1 = VectorstoreSingleton.get_instance(persist_directory)
        instance2 = VectorstoreSingleton.get_instance(persist_directory)
        assert instance1 is instance2


def test_ollama_singleton_exception():
    with pytest.raises(Exception):
        OllamaSingleton()  # Should raise an exception if already initialized

def test_vectorstore_singleton_exception():
    # Use a temporary directory for the persist_directory
    with tempfile.TemporaryDirectory() as persist_directory:
        instance1 = VectorstoreSingleton.get_instance(persist_directory)
        with pytest.raises(Exception):
            VectorstoreSingleton(persist_directory)  # Should raise an exception if already initialized


def test_create_rag_chain():
    # Use a temporary directory for the persist_directory
    with tempfile.TemporaryDirectory() as persist_directory:
        # Create the RAG chain
        chain = create_rag_chain(persist_directory)
        # Assert that the chain is created and is not None
        assert chain is not None


def test_rag_session_initialization():
    session_id = "test_session"
    # Use a temporary directory for the persist_directory
    with tempfile.TemporaryDirectory() as persist_directory:
        rag_session = RAGSession(session_id, persist_directory)
        assert rag_session.session_id == session_id
        assert rag_session.persist_directory == persist_directory
        assert rag_session.chain is not None
        assert rag_session.history is not None
        assert rag_session.runnable_with_history is not None


def test_vectorstore_configuration():
    # Use a temporary directory for the persist_directory
    with tempfile.TemporaryDirectory() as persist_directory:
        vectorstore = VectorstoreSingleton.get_instance(persist_directory).vectorstore
        assert vectorstore is not None
        # Add more assertions based on your configuration requirements




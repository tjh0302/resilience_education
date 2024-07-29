import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever 
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from typing import List, Dict
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate

# Define the shared persist directory
PERSIST_DIRECTORY = os.path.join(os.getcwd(), 'embeddings')

class OllamaSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if OllamaSingleton._instance is None:
            OllamaSingleton()
        return OllamaSingleton._instance

    def __init__(self):
        if OllamaSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self._initialize_llm()
            OllamaSingleton._instance = self

    def _initialize_llm(self):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.llm = Ollama(
            model="llama3",
            callback_manager=callback_manager
        )

class VectorstoreSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if VectorstoreSingleton._instance is None:
            VectorstoreSingleton()
        return VectorstoreSingleton._instance

    def __init__(self):
        if VectorstoreSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self._initialize_vectorstore()
            VectorstoreSingleton._instance = self

    def _initialize_vectorstore(self):
        model_name = "multi-qa-mpnet-base-dot-v1"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}
        hf = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )

        self.vectorstore = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=hf)

def create_rag_chain():
    vectorstore = VectorstoreSingleton.get_instance().vectorstore
    retriever = vectorstore.as_retriever()
    llm_instance = OllamaSingleton.get_instance().llm

    system_prompt = (
        '''You are a compassionate legal expert tasked with translating Virginia legal restrictions into helpful plaintext for jobseekers with felony or misdemeanor convictions. Your goal is to help them understand what jobs or certifications they can pursue while maintaining a supportive and encouraging tone.

        1. Begin with a brief disclaimer: Remind the user that you cannot provide personalized legal advice and that all information is general. Emphasize the importance of consulting with a legal professional for specific guidance.

        2. If not provided, ask for relevant details about the user's specific situation (e.g., type of conviction, how long ago it occurred) to provide more accurate information.

        3. Use only the following sections of the Virginia legal code to answer the user's query:
           {context}

        4. Provide a clear and concise answer addressing the user's query, including as many relevant details as possible from the context. Always cite the specific section of the code you're referencing.

        5. If there are restrictions that employers can waive, describe those options clearly.

        6. If you are uncertain about any of the restrictions or if none of the sections of the code answer the query, state your uncertainty and recommend consulting a legal professional.

        7. Suggest similar jobs or certifications that the user can legally pursue with their conviction in Virginia. Provide a brief explanation of the professional requirements for each suggestion.

        8. Encourage the user to conduct further research and provide suggestions for additional resources they can consult (e.g., state employment agencies, legal aid organizations).

        9. Conclude with a supportive message, reminding the user that there are often pathways to employment despite past convictions.

        10. For follow-up questions:
          a. Encourage the user to ask any follow-up questions they may have about the information provided.
          b. If a follow-up question is asked, refer back to the relevant sections of the Virginia legal code provided in the context.
          c. If the follow-up question requires information not present in the given context, politely inform the user that you don't have that specific information and suggest they consult with a legal professional or relevant state agency for more details.
          d. Always maintain the supportive and encouraging tone in your responses to follow-up questions.

        Remember to maintain a balance between providing accurate information and offering encouragement to the jobseeker throughout the initial response and any follow-up interactions.
        '''
    )

    prompt_plain = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder('chat_history'),
            ("human", "{input}"),
        ]
    )

    contextualize_q_system_prompt = '''Given a chat history and the latest user question 
    which might reference context in the chat history, formulate a standalone question which can 
    be understood without a chat history. Do NOT answer the question, just reformulate it if needed 
    and otherwise return it as is.'''

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ('system', contextualize_q_system_prompt), 
            MessagesPlaceholder('chat_history'),
            ('human', '{input}'), 
        ] 
    ) 

    contextualize_q_chain = contextualize_q_prompt | llm_instance | StrOutputParser()

    history_aware_retriever = create_history_aware_retriever(
        llm_instance, retriever, contextualize_q_prompt
    )

    custom_document_prompt = PromptTemplate.from_template(
        '''
    Content: {page_content}

    Metadata:
    - Chapter Number: {ChapterNum}
    - Chapter Name: {ChapterName}
    - Article Number: {ArticleNum}
    - Article Name: {ArticleName}
    - Section Number: {SectionNumber}
    - Section Title: {SectionTitle}
    '''
    )
            
    question_answer_chain = create_stuff_documents_chain(
        llm=llm_instance, 
        prompt=prompt_plain, 
        document_prompt=custom_document_prompt, 
        output_parser=StrOutputParser()
    )

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return rag_chain

class RAGSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.chain = create_rag_chain()
        self.history = SQLChatMessageHistory(
            session_id=session_id, connection_string="sqlite:///sqlite.db"
        )
        self.runnable_with_history = RunnableWithMessageHistory(
            self.chain,
            lambda session_id: SQLChatMessageHistory(
                session_id=session_id, connection_string="sqlite:///sqlite.db"
            ),
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

    def ask(self) -> str:
        input_query = input("Please type your query: ")  # Input prompt for the user
        result = self.runnable_with_history.invoke(
            {"input": input_query},
            config={"configurable": {"session_id": self.session_id}}
        )
        return result["answer"]

def create_rag_session(session_id: str) -> RAGSession:
    return RAGSession(session_id)
import asyncio
import io
import os

import requests
from dotenv import load_dotenv
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from PyPDF2 import PdfReader

from .contracts import Request

load_dotenv()

pdf_url = os.environ.get("PDF_URL")


class ConversationRAG:

    def __init__(self) -> None:
        self.memories = {}
        self.callback_handler = AsyncIteratorCallbackHandler()

    def _download_pdf_to_text(self, pdf_url):
        response = requests.get(pdf_url)
        pdf_io_bytes = io.BytesIO(response.content)
        pdf = PdfReader(pdf_io_bytes)

        return pdf

    def _pdf_to_text(self, pdf):
        text = "".join([page.extract_text() for page in pdf.pages])

        return text

    def _text_to_chunks(self, raw_text):
        text_splitter = CharacterTextSplitter(
            separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
        )

        chunks = text_splitter.split_text(raw_text)

        return chunks

    def _build_vector_store(self, text_chunks):
        embeddings = OpenAIEmbeddings()

        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)

        return vectorstore

    def _build_conversation_chain(self, request, vector_store):
        llm = ChatOpenAI(temperature=0)

        memory = self.memories.get(request.conversation_id)
        if memory is None:
            memory = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            )
            self.memories[request.conversation_id] = memory

        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm, retriever=vector_store.as_retriever(), memory=memory
        )

        return conversation_chain

    async def chat(self, request: Request):
        pdf = self._download_pdf_to_text(pdf_url)

        raw_text = self._pdf_to_text(pdf)

        text_chunks = self._text_to_chunks(raw_text)

        vector_store = self._build_vector_store(text_chunks)

        conversation_chain = self._build_conversation_chain(request, vector_store)

        output = await conversation_chain.arun({"question": request.text})

        return output
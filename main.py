from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import JSONLoader
from langchain import hub
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_community.document_loaders import TextLoader

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str



def main():

    load_dotenv()  


    llm = ChatOpenAI(model="gpt-4o-mini")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = InMemoryVectorStore(embeddings)

    # path = "csci_courses_with_descriptions.json"

    # loader = JSONLoader(
    #         file_path=path,
    #         jq_schema='.courses',
    #         text_content=False)

    # docs = loader.load()
    # print(type(docs))

    path = "output.txt"  # Path to your .txt file

    loader = TextLoader(file_path=path)

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    all_splits = text_splitter.split_documents(docs)

    _ = vector_store.add_documents(documents=all_splits)
    prompt = hub.pull("rlm/rag-prompt")

    def retrieve(state: State):
        retrieved_docs = vector_store.similarity_search(state["question"])
        return {"context": retrieved_docs}


    def generate(state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt.invoke({"question": state["question"], "context": docs_content})
        response = llm.invoke(messages)
        return {"answer": response.content}

    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()
    

   
    response = graph.invoke({"question": "I have to learn visual computing, what courses should i focus on?"})
    print(response["answer"])


if __name__=='__main__':
    main()

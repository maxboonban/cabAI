from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph, END
from typing_extensions import List, TypedDict
from langchain import hub
from langchain_core.documents import Document
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Initialize LLM and vector store
llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = InMemoryVectorStore(embeddings)

# Load and process text data
path = "output.txt"  # Path to your .txt file
loader = TextLoader(file_path=path)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
all_splits = text_splitter.split_documents(docs)
vector_store.add_documents(documents=all_splits)

def retrieve(query: str):
    """Retrieve relevant documents based on a query using similarity search."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

tools = ToolNode([retrieve])  # This should now work without errors

# Define message state graph
from langgraph.graph import MessagesState

def query_or_respond(state: MessagesState):
    llm_with_tools = llm.bind_tools([retrieve])
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

tools = ToolNode([retrieve])

def generate(state: MessagesState):
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
        "You are an assistant for question-answering tasks. "
        "Use the following retrieved context to answer the question. "
        "Use three sentences maximum."
        "Be a little funny."
        "Answers should be relevant to courses offered"
        "Students can ask about their professors using their first and last name"
        "Instructors are professors"
        "Students might use instructor and professor interchangably"
        "mention the class code with name anytime a course related question is asked"
        "\n\n"
        f"{docs_content}"
    )
    conversation_messages = [
        message for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    response = llm.invoke(prompt)
    return {"messages": [response]}

# Construct the processing graph
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("query_or_respond", query_or_respond)
graph_builder.add_node("tools", tools)
graph_builder.add_node("generate", generate)
graph_builder.set_entry_point("query_or_respond")
graph_builder.add_conditional_edges("query_or_respond", tools_condition, {END: END, "tools": "tools"})
graph_builder.add_edge("tools", "generate")
graph_builder.add_edge("generate", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    config = {"configurable": {"thread_id": "abc123"}}
    response = graph.invoke({"messages": [{"role": "user", "content": question}]}, config=config)
    return jsonify({"answer": response["messages"][-1].content})

# if __name__ == "__main__":
#     # app.run(debug=True)
#     app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000) 

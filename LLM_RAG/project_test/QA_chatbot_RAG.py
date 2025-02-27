import os
import docx
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.schema import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph
import langsmith

# 문서로드 함수
def load_docx(filepath):
    doc = docx.Document(filepath)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text

# 벡터 db 생성 함수수
def create_vector_db(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.from_texts(chunks, embeddings)
    return vector_db


# qa chain 생성함수 
def create_qa_chain(vector_db):
    retriever = vector_db.as_retriever()
    llm = ChatOpenAI(temperature=0, model_name="gpt-4")
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain

#  LangGraph state 
class ChatState:
    def __init__(self, query):
        self.query = query
        self.response = ""

# LangGraph 노드 구성성
def check_relevance(state: ChatState):
    """Check if the query is related to the document."""
    llm = ChatOpenAI(temperature=0)
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage("You are an AI assistant that determines if a query is related to a given document."),
        ("user", "Query: {query}\nIs this related to the document? Reply with 'yes' or 'no'.")
    ])
    result = llm.invoke(prompt.format(query=state.query))
    return "related" if "yes" in result else "unrelated"

def generate_response(state: ChatState, qa_chain):
    """Generate response if the question is relevant."""
    state.response = qa_chain.run(state.query)
    return state

def request_relevant_question(state: ChatState):
    """Request the user to ask a related question."""
    state.response = "Your question is not related to the document. Please ask a question relevant to the document."
    return state

#  LangGraph workflow 구성성
def build_graph(qa_chain):
    graph = StateGraph(ChatState)
    
    graph.add_node("check_relevance", check_relevance)
    graph.add_node("generate_response", lambda state: generate_response(state, qa_chain))
    graph.add_node("request_relevant_question", request_relevant_question)
    
    graph.add_edge("check_relevance", "related", "generate_response")
    graph.add_edge("check_relevance", "unrelated", "request_relevant_question")
    
    graph.set_entry_point("check_relevance")
    return graph.compile()

# Main function
def main():
    filepath = "qa_document.docx"  # 수정
    text = load_docx(filepath)
    vector_db = create_vector_db(text)
    qa_chain = create_qa_chain(vector_db)
    
    # Initialize LangGraph
    workflow = build_graph(qa_chain)
    
    # Debugging with LangSmith
    langsmith.init()
    
    while True:
        query = input("Ask a question: ")
        if query.lower() in ["exit", "quit"]:
            break
        state = ChatState(query)
        response_state = workflow.invoke(state)
        print("Response:", response_state.response)

if __name__ == "__main__":
    main()

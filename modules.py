from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent import AgentRunner
from llama_index.core import Settings
from pathlib import Path
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex
from utils import get_doc_tools

def manydocAgent(titles: list[str]) -> AgentRunner:
    tool_dict = {}
    for title in titles:
        #print(f"Getting tools for paper: {title}")
        summary_tool, vector_tool = get_doc_tools(f"data\\{title}.pdf", title)
        tool_dict[title] = [vector_tool, summary_tool]
    
    tools = [t for title in titles for t in tool_dict[title]]

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

    obj_index = ObjectIndex.from_objects(
        tools,
        index_cls=VectorStoreIndex,
    )

    obj_retriever = obj_index.as_retriever(similarity_top_k=3)

    agent_worker = FunctionCallingAgentWorker.from_tools(
    tool_retriever=obj_retriever,
    llm=llm, 
    system_prompt=""" \
    You are an agent designed to answer queries over a set of given papers.
    Please always use the tools provided to answer a question. Do not rely on prior knowledge.\
    """,
        verbose=True
    )

    agent = AgentRunner(agent_worker)
    
    #call agent.chat(query) in main
    
    return agent

def multidocAgent(urls: list[str], titles: list[str]) -> AgentRunner:
    tool_dict = {}
    for title in titles:
        #print(f"Getting tools for paper: {title}")
        summary_tool, vector_tool = get_doc_tools(title, Path(title).stem)
        tool_dict[title] = [vector_tool, summary_tool]
    
    tools = [t for title in titles for t in tool_dict[title]]

    llm = OpenAI(model="gpt-3.5-turbo")

    agent_worker = FunctionCallingAgentWorker.from_tools(
        tools, 
        llm=llm, 
        verbose=True
    )
    agent = AgentRunner(agent_worker)
    
    #call agent.chat(query) in main
    
    return agent
    

#Chat agent keeps track of conversation history, and breaks down query into multiple tasks
#Each task is routed to a tool
def simpleAgent(query: str, title: str) -> AgentRunner:
    summary_tool, vector_tool = get_doc_tools(title, Path(title).stem)
    
    llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

    agent_worker = FunctionCallingAgentWorker.from_tools(
        [vector_tool, summary_tool], 
        llm=llm, 
        verbose=True
    )
    agent = AgentRunner(agent_worker)

    return agent

#LLM routes queries to one of multiple tools 
def simpleRouter(query: str, title: str) -> str:
    Settings.llm = OpenAI(model="gpt-3.5-turbo")
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")
    
    summary_tool, vector_tool = get_doc_tools(title, Path(title).stem)

    query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=[
            summary_tool,
            vector_tool,
        ],
        verbose=True
    )

    query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=[
            summary_tool,
            vector_tool,
        ],
        verbose=True
    )

    response = query_engine.query("What is the summary of the document?")
    return response
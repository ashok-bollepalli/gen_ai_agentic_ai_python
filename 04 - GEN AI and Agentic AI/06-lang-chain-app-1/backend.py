from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# load env variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("OPENAI_MODEL")

# create llm client
llm_model = ChatOpenAI(
    api_key=openai_api_key,
    model=openai_model,
    temperature=0.5
)

# Create Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an expert technical trainer. "
     "Explain concepts in simple English for freshers."),

    ("human",
     "Explain {topic} with a simple real-world example.")
])

# Create Output Parser
parser = StrOutputParser()

# Create LangChain pipeline
chain = prompt | llm_model | parser

# Reusable function
def explain_topic(topic_name):

    result = chain.invoke({
        "topic": topic_name
    })

    return result
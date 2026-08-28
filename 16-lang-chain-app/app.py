from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# create LLM object using local ollama model (llama3.2)
llm = ChatOllama(model="llama3.2")

#create prompt template
prompt = ChatPromptTemplate.from_template("""

You are a friendly GEN AI Trainer

Explain the topic clearly for beginner students.

Rules:
1. Use simple english
2. Give step-by-step explanation
3. Give one real-time example
4. Avoid mistakes in coding

Topic : {topic}

""")

# create langchain pipeline
chain = prompt | llm | StrOutputParser()

# Take input from user
topic = input("Enter Topic : ")

answer = chain.invoke({"topic" : topic})

print(answer)
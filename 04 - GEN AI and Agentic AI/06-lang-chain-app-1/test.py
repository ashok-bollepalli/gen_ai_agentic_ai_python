import requests

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

llm = ChatOllama(model="llama3.2")

def get_course_details(input):
    course_name = input["course"]

    url = f"http://localhost:8080/course/{course_name}"

    response = requests.get(url)
    data = response.json()

    return {
        "course": data["courseName"],
        "duration": data["duration"],
        "trainer": data["trainer"],
        "topics": data["topics"]
    }

prompt = ChatPromptTemplate.from_template(
    """
    You are an Ashok IT course counsellor.

    Course: {course}
    Duration: {duration}
    Trainer: {trainer}
    Topics: {topics}

    Explain this course to a student in a convincing way.
    """
)

chain = RunnableLambda(get_course_details) | prompt | llm | StrOutputParser()

response = chain.invoke({
    "course": "GenAI"
})

print(response)
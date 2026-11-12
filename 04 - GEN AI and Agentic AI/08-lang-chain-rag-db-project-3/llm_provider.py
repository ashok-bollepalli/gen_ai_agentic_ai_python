from langchain_openai import ChatOpenAI

from config import OPENAI_CHAT_MODEL


# =========================================================
# CREATE OPENAI LLM
# =========================================================

def get_llm():

    llm = ChatOpenAI(

        model=OPENAI_CHAT_MODEL,

        temperature=0
    )


    return llm

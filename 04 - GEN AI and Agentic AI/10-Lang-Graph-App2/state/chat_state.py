from typing import TypedDict

class ChatState(TypedDict, total=False):
    question: str
    student_id: int
    category: str
    context: str
    answer: str

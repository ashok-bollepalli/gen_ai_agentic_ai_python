from state.chat_state import ChatState
from database.student_repository import find_student

def database_node(state:ChatState) -> dict:
    print("Executing database node")
    student_id = state.get("student_id")

    if student_id is None:
        return {
            "context": (
                "Student ID was not provided. "
                "Payment information cannot be retrieved."
            )
        }

    student = find_student(student_id)

    context = f"""
Student ID : {student['student_id']}
Student name: {student['name']}
Course: {student['course']}
Fee paid: INR {student['fee_paid']}
Fee due: INR {student['fee_due']}
Batch time: {student['batch_time']}
""".strip()

    return {"context": context}

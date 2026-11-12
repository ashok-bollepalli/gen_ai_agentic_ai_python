from fastapi import FastAPI

a = FastAPI()

@a.get("/welcome")
def get_welcome_msg():
    return {"message" : "Welcome to FastAPI"}

@a.get("/greet")
def get_greet_msg():
    return {"message" : "Good Morning"}
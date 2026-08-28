class AIModel:
    def generate_response(self, prompt):
        print("Generating response using general AI Model")

class OpenAIModel(AIModel):
    def generate_response(self, prompt):
        print("Generating response using OpenAI GPT Model")
        print("Prompt:", prompt)

class GeminiModel(AIModel):
    def generate_response(self, prompt):
        print("Generating response using Gemini Model")
        print("Prompt:", prompt)

model1 = OpenAIModel()
model1.generate_response("Explain Python Decorators")
print("====================================================")
model2 = GeminiModel()
model2.generate_response("Explain Python File handling")
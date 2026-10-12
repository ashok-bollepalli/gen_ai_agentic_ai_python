import boto3

# 1. Connect to Bedrock
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# 2. Pick the model (must be enabled in your AWS account)
MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

# 3. Function: takes question, returns answer
def ask_bot(question):
    response = client.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [{"text": question}]
            }
        ]
    )
    return response["output"]["message"]["content"][0]["text"]


# 4. Use it
if __name__ == "__main__":
    answer = ask_bot("What is Spring Boot?")
    print(answer)
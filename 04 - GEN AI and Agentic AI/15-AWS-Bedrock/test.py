import boto3

bedrock = boto3.client("bedrock", region_name="us-east-1")  # note: "bedrock", not "bedrock-runtime"

for p in bedrock.list_inference_profiles()["inferenceProfileSummaries"]:
    if "anthropic" in p["inferenceProfileId"]:
        print(p["inferenceProfileId"])
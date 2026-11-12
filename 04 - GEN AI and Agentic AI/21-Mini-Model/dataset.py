from tokenizer import encoded_tokens

inputs = []
outputs = []

for i in range(len(encoded_tokens) - 1):
    inputs.append(encoded_tokens[:i + 1])
    outputs.append(encoded_tokens[i + 1])

print("=" * 50)
print("Inputs:", inputs)
print("=" * 50)
print("Outputs:", outputs)
print("=" * 50)

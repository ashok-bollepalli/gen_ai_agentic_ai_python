"""
train.py

Purpose
-------
Train the Mini LLM.

Steps
-----
1. Load Dataset
2. Create Model
3. Define Loss Function
4. Define Optimizer
5. Train
6. Stop when loss is sufficiently low
7. Save Model
"""

import torch
import torch.nn as nn
import torch.optim as optim

from tokenizer import vocab
from dataset import inputs, outputs
from model import MiniLLM


# ---------------------------------
# Hyper Parameters
# ---------------------------------

VOCAB_SIZE = len(vocab)

EMBEDDING_DIM = 16

EPOCHS = 1000

LEARNING_RATE = 0.01

LOSS_THRESHOLD = 0.001


# ---------------------------------
# Create Model
# ---------------------------------

model = MiniLLM(
    vocab_size=VOCAB_SIZE,
    embedding_dim=EMBEDDING_DIM
)


# ---------------------------------
# Loss Function
# ---------------------------------

criterion = nn.CrossEntropyLoss()


# ---------------------------------
# Optimizer
# ---------------------------------

optimizer = optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)


# ---------------------------------
# Training Loop
# ---------------------------------

for epoch in range(EPOCHS):

    total_loss = 0.0

    for x, y in zip(inputs, outputs):

        # Convert input and output to tensors
        x = torch.tensor([x], dtype=torch.long)

        y = torch.tensor([y], dtype=torch.long)

        # Forward propagation
        prediction = model(x)

        # Calculate loss
        loss = criterion(prediction, y)

        # Clear previous gradients
        optimizer.zero_grad()

        # Backward propagation
        loss.backward()

        # Update weights
        optimizer.step()

        # Add loss
        total_loss += loss.item()

    # Display loss
    print(
        f"Epoch {epoch + 1}/{EPOCHS} "
        f"Loss = {total_loss:.8f}"
    )

    # ---------------------------------
    # Early Stopping
    # ---------------------------------

    if total_loss < LOSS_THRESHOLD:

        print("\nLoss reached the threshold.")
        print("Training stopped early.")

        break


# ---------------------------------
# Save Model
# ---------------------------------

torch.save(
    model.state_dict(),
    "mini_model.pth"
)

print("\nTraining Completed.")
print("Model Saved Successfully.")
import torch.nn as nn

class MiniLLM(nn.Module):

    def __init__(self, vocab_size, embedding_dim):

        super().__init__()

        # Convert word IDs into vectors
        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embedding_dim
        )

        # Hidden Layer
        self.linear1 = nn.Linear(
            embedding_dim,
            512
        )

        # Activation Function
        self.relu = nn.ReLU()

        # Output Layer
        self.linear2 = nn.Linear(
            512,
            vocab_size
        )

    # forward propagation
    def forward(self, x):

        # Word IDs → vectors
        x = self.embedding(x)

        # Average all word vectors
        x = x.mean(dim=1)

        # Hidden Layer
        x = self.linear1(x)

        # Activation
        x = self.relu(x)

        # Final Prediction
        x = self.linear2(x)

        return x
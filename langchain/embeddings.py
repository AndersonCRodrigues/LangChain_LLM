from gemini import google_embedding
import numpy as np

embedding_model = google_embedding

embeddings = embedding_model.embed_documents(
    [
        "Eu gosto de cachorro",
        "Eu gosto de animais",
        "Hoje a tarde está chovendo",
    ]
)

# print(len(embeddings))
# Sprint(embeddings[0][:10])

for i in range(len(embeddings)):
    for j in range(len(embeddings)):
        print(round(np.dot(embeddings[i], embeddings[j]), 2), end=" | ")
    print()

import os
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

googleai_client = ChatGoogleGenerativeAI(
    google_api_key=GOOGLE_API_KEY,
    model="gemini-2.0-flash-lite",
)

google_embedding = GoogleGenerativeAIEmbeddings(
    google_api_key=GOOGLE_API_KEY,
    model="models/text-embedding-004",
)

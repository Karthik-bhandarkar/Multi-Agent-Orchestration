import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# Instantiate the model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",   # or another available Gemini model
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

# Define system prompt
system_msg = SystemMessage(content="You are a helpful assistant that answers concisely.")

# Take user input
user_input = input("User: ")
human_msg = HumanMessage(content=user_input)

# Generate the response
response = llm.invoke([system_msg, human_msg])

print("\nAssistant:", response.content)

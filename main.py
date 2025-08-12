from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

GeminiKey = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GeminiKey,
    tempreture=0.5
    )

response = llm.invoke([{"role":"user", "content":"Hi there. How are you?"}])
print(response.content)

with open(file.txt) as file
    content = file.read()


#print("Hi I am Albert, how may I help you today?")
#while True:
#    userInput = input("You: ")
#    if userInput =="exit":
#        break
#    print(f"Cool, Thanks for sharing that {userInput}")

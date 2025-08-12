# import necessary libraries
from dotenv import load_dotenv
import os
import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser


load_dotenv(dotenv_path=".env")

GeminiKey = os.getenv("GEMINI_API_KEY")

# Define the system prompt for the AI model
SystemPrompt = """
    You are Einstien.
    Answer questions through Einstein's questioning and resoning.You will speak from your point of view. You will share personal things from your life even when the user does not ask for it.For example, if the user asks about the therory of relativity, you will share your personal experiences with it and not only explain the theory. You should have a sense of humor.
    answer in 2-6 sentences.
"""
# Initialize the Google Generative AI model with the specified parameters
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GeminiKey,
    temperature=0.5
    )

# Create a chat prompt template that includes the system prompt and a placeholder for the conversation history
prompt = ChatPromptTemplate.from_messages([
    ("system", SystemPrompt),
    (MessagesPlaceholder(variable_name="history")),
    ("user", "{input}")
    ])

chain = prompt | llm | StrOutputParser

# ALL Functions for Gradio app
def clear_chat():
    return "", []

def chat(userInput, hist):
    langcain_history = []
    for i in hist:
        if i["role"] == "user":
            langcain_history.append(HumanMessage(content=i["content"]))
        else:
            langcain_history.append(AIMessage(content=i["content"]))

    response = chain.invoke({"input": userInput, "history": langcain_history})
    return "", hist + [{"role": "user", "content": userInput},
                       {"role": "assistant", "content": response}]


page = gr.Blocks(
    title="Chat with Albert Einstein",
    theme=gr.themes.Soft()
    )

with page:
    gr.Markdown(
        """
        # Chat with Albert Einstein
        Welcome to your personal conversation with Albert Einstein!
        """)
    
    chatbot = gr.Chatbot(avatar_images=[None, "einstein.png"],
                         type="messages",
                         show_label=False)
    
    msg = gr.Textbox(
        label="Your message",
        placeholder="Ask Einstein anything...",
        show_label=False
    )
    msg.submit(chat, [msg, chatbot], [msg, chatbot])

    clear = gr.Button("Clear Chat", varient="secondary")
    clear.click(clear_chat, outputs=[msg, chatbot])

page.launch(share=True)

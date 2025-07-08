import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from twilio.rest import Client
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_core.runnables import Runnable
from langchain_groq import ChatGroq

load_dotenv()

class SendWhatsAppMessageInput(BaseModel):
    message: str
    phone_number: str

@tool("send_whatsapp_message", args_schema=SendWhatsAppMessageInput)
def send_whatsapp_tool(message: str, phone_number: str) -> str:
    """Send a WhatsApp message using Twilio to the specified phone number."""
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_FROM")

    from_number = f"whatsapp:{from_number.lstrip('whatsapp:')}"
    phone_number = f"whatsapp:{phone_number.lstrip('whatsapp:')}"

    client = Client(sid, token)
    msg = client.messages.create(body=message, from_=from_number, to=phone_number)
    return f"Message sent. SID: {msg.sid}"

def main():
    groq_key = os.getenv("GROQ_API_KEY")
    to_number = os.getenv("TWILIO_WHATSAPP_TO")

    llm = ChatGroq(api_key=groq_key, model_name="llama3-70b-8192")
    llm = llm.bind_tools([send_whatsapp_tool])

    prompt = HumanMessage(
        content=f"Send a WhatsApp message to {to_number} saying 'Hello! This is an automated message from your AI assistant powered by LangChain + Groq.'"
    )
    response = llm.invoke([prompt])

    call = response.additional_kwargs["tool_calls"][0]
    args = json.loads(call["function"]["arguments"])
    print(send_whatsapp_tool.invoke(args))

if __name__ == "__main__":
    main()

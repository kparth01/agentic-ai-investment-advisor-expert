import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class Config:

    def __init__(self) -> None:
        self.llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), 
                            temperature=os.getenv("TEMPERATURE"),
                            openai_api_key=os.getenv("OPENAI_API_KEY"))
        
    def chain_prompt(self, system_prompt: str, prompt: str, stateStep: str) -> dict:
        messages = []
        
        if system_prompt: 
            messages.append(SystemMessage(content=system_prompt))
        if prompt: 
            messages.append(HumanMessage(content=prompt))
        
        chain = self.llm | StrOutputParser()
        result = chain.invoke(messages)
        
        return {
            stateStep: result
        }

        
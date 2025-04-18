from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
import os
from dotenv import load_dotenv  
load_dotenv()

##groq api
groq_api_key=os.getenv("GROQ_API")


##initialize groq api key
model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

system_template="Translate the following into {language}"

prompt_template=ChatPromptTemplate([
    ("system",system_template),
    ("user","{text}")
])

parser=StrOutputParser()

##create a chain
chain=prompt_template|model|parser

##app definition
app=FastAPI(title="Langchain Server",
            version="1.0",
            description="A simnple API Server using LangChain runnable interfaces"
            )


##adding chain routes
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)




from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.retrieval import retrieve_news

app = FastAPI()

# might need to specify the origin domain (according to the fastapi documentation)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    text: str

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/submit")
async def submit(input: UserInput):
    summary, result_list = retrieve_news(input.text, "en")
    return {"summary": summary, "articles": result_list}
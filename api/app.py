from fastapi import FastAPI
from sqlalchemy import select
from models import Author, Book, run_with_async
app = FastAPI()

@app.get('/')
async def index():
    return {'msg' : 'Welcome to my API!'}

@app.get('/authors', response_model=List[Author])
async def get_authors():
    authors = run_with_async(
        lambda session: session.execute(select(Author)).scalars().all()
    )
    return authors
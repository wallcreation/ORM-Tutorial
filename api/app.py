from fastapi import FastAPI
from sqlalchemy import select
from models import Author, Book, run_with_async
from schemas import AuthorsBase
app = FastAPI()

@app.get('/')
async def index():
    return {'msg' : 'Welcome to my API!'}

@app.get('/authors', response_model=list[AuthorsBase])
async def get_authors():
    authors = await run_with_async(
        lambda session: session.execute(select(Author))
    )
    return authors.scalars().all()
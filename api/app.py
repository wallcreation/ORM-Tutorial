from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from models import Author, Book, run_with_async
from schemas import AuthorsBase

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/banner')
async def banner():
    return {
        'msg' : 'Simple Front'
    }

@app.get('/')
async def index():
    authors = await run_with_async(
        lambda session: session.execute(select(Author))
    )
    books = await run_with_async(
        lambda session: session.execute(select(Book))
    )
    total_books = len(books.scalars().all())
    total_authors = len(authors.scalars().all())
    return {
        'msg' : 'Welcome to my API!',
        'banner' : 'Sinple API for Books and Authors',
        'version' : '1.0.0',
        'total_authors' : total_authors,
        'total_books' : total_books
        }

@app.get('/authors', response_model=list[AuthorsBase])
async def get_authors():
    authors = await run_with_async(
        lambda session: session.execute(select(Author))
    )
    return authors.scalars().all()

@app.get('/total_authors')
async def get_total_authors():
    authors = await run_with_async(
        lambda session: session.execute(select(Author))
    )
    return {
        'count': len(authors.scalars().all())
    }

@app.get('/total_books')
async def get_total_books():
    books = await run_with_async(
        lambda session: session.execute(select(Book))
    )
    return {
        'count' : len(books.scalars().all())
    }
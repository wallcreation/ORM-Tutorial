from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from models import Author, Book, run_with_async, session_maker
import schemas

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

@app.get('/authors', response_model=list[schemas.AuthorsBase])
async def get_authors():
    authors = await run_with_async(
        lambda session: session.execute(select(Author))
    )
    list_of_authors = authors.scalars().all()
    print(list_of_authors)
    return list_of_authors

@app.get('/books', response_model=list[schemas.BooksBase])
async def get_books():
    books = await run_with_async(
        lambda session: session.execute(select(Book))
    )
    list_of_books = books.scalars().all()
    return list_of_books

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

# @app.post('/add/books')
# async def add_book(book: schemas.BooksAddBase):
#     is_found = await run_with_async(
#         lambda session: session.execute(
#             select(Book).filter_by(
#                 serial_number=book.serial_number
#             )
#         )
#     )

#     print(is_found)
#     if is_found.scalars().first() is not None:
#         raise HTTPException(400, 'Book already exist')

#     author_ = book.author.split(' ')
#     print(author_)
#     author = await run_with_async(
#         lambda session: session.execute(
#             select(Author).filter_by(
#                 first_name=author_[0],
#                 last_name=author_[1]
#             )
#         )
#     )

#     author = author.scalars().first()
#     if author is None:
#         raise HTTPException(400, "Author not found for this book")

#     new_book = Book(
#         name=book.name,
#         author=book.author,
#         published_at=book.published_at,
#         serial_number=book.serial_number,
#         author_ref=author
#     )

#     async with session_maker() as session:
#         await session.add(new_book)
#         await session.commit()
#         await session.refresh(new_book)

#     return True

@app.post('/add/books')
async def add_book(book: schemas.BooksAddBase):
    async with session_maker() as session:
        # 1. Vérifier si le livre existe déjà
        result = await session.execute(
            select(Book).filter_by(serial_number=book.serial_number)
        )
        if result.scalars().first():
            raise HTTPException(400, 'Book already exists')

        # 2. Trouver l’auteur
        try:
            first_name, last_name = book.author.split(' ', 1)
        except ValueError:
            raise HTTPException(400, "Author format should be 'First Last'")

        result = await session.execute(
            select(Author).filter_by(first_name=first_name, last_name=last_name)
        )
        author = result.scalars().first()
        if author is None:
            raise HTTPException(400, "Author not found for this book")

        # 3. Ajouter le livre
        new_book = Book(
            name=book.name,
            author=book.author,
            published_at=book.published_at.replace(tzinfo=None),
            serial_number=book.serial_number,
            author_ref=author
        )
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)

        return {"message": "Book added", "id": new_book.id}


@app.post('/add/author/')
async def add_author(author: schemas.AuthorsAddBase):
    async with session_maker() as session:
        existing_authors = session.execute(
            select(Author).filter_by(
                first_name=author.first_name,
                last_name=author.last_name
            )
        )
        if existing_authors.scalars().first():
            return HTTPException(400, "Author already exist")
        
    
    # is_found = await run_with_async(
    #     lambda session: session.execute(
    #         select(Author).filter_by(
    #             last_name=author.last_name
    #             )
    #         )
    #     )

    # if is_found.scalars.first() is not None:
    #     raise HTTPException(400, 'Author already exist')

    # new_author = Author(
    #     first_name=author.first_name,
    #     last_name=author.last_name,
    #     birth_date=author.birth_date
    # )
    # await run_with_async(
    #     lambda session: session.add(new_author)
    # )
    # return

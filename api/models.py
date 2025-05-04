from contextlib import asynccontextmanager

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import relationship

database_url = "postgresql+asyncpg://postgres.xsoytqvarevowemcjxwo:3!6T!mwLy_g_E8w@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"

engine = create_async_engine(database_url)

@asynccontextmanager
async def session_maker():
    session = AsyncSession(bind=engine, expire_on_commit=False)
    try:
        yield session
    except Exception as e:
        print("Error:", e)
        await session.rollback()
    finally:
        await session.close()

async def run_with_async(fun, *args, **kwargs):
    async with session_maker() as session:
        return await fun(session, *args, **kwargs)

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String)
    author = sql.Column(sql.String)
    published_at = sql.Column(sql.DateTime)
    serial_number = sql.Column(sql.Integer)

    author_id = sql.Column(sql.Integer, sql.ForeignKey("authors.id"))
    author_ref = relationship('Author', back_populates='books')

    def __repr__(self):
        return f"<Book(name={self.name}, author={self.author}, published_at={self.published_at}, serial_number={self.serial_number})>"

class Author(Base):
    __tablename__ = "authors"
    
    id = sql.Column(sql.Integer, primary_key=True)
    first_name = sql.Column(sql.String)
    last_name = sql.Column(sql.String)
    birth_date = sql.Column(sql.DateTime)

    books = relationship('Book', back_populates='author_ref')

    def __repr__(self):
        return f"<Author(first_name={self.first_name}, last_name={self.last_name}, birth_date={self.birth_date})>"

# Base.metadata.create_all(engine)


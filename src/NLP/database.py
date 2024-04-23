from datetime import date
from typing import List
from sqlalchemy import create_engine
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


file_tag = Table(
    'file_tag',
    Base.metadata,
    Column('file', ForeignKey('file.id'), primary_key=True),
    Column('tag', ForeignKey('tag.id'), primary_key=True)
)

tag_category = Table(
    'tag_category',
    Base.metadata,
    Column('tag', ForeignKey('tag.id'), primary_key=True),
    Column('category', ForeignKey('category.id'), primary_key=True)
)


class File(Base):
    __tablename__ = 'file'

    id: Mapped[int] = mapped_column(primary_key=True)
    file_path: Mapped[str]
    text: Mapped[str]
    date_added: Mapped[date]
    num_accesses: Mapped[int]
    tags: Mapped[List['Tag']] = relationship(secondary=file_tag, back_populates='files')

    def __repr__(self):
        return f'({self.file_path}, {self.text}, {self.date_added}, {self.num_accesses}, {self.tags})'


class Tag(Base):
    __tablename__ = 'tag'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    #category: Mapped[int] = mapped_column(ForeignKey('category.id'))
    files: Mapped[List['File']] = relationship(secondary=file_tag, back_populates='tags')
    categories: Mapped[List['Category']] = relationship(secondary=tag_category, back_populates='tags')

    def __repr__(self):
        return f'({self.description})'

    
class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    tags: Mapped[List['Tag']] = relationship(secondary=tag_category, back_populates='categories')

    def __repr__(self):
        return f'({self.name}, {self.tags})'


# Creates the SQLite3 database if it doesn't exist
def create_database():
    engine = create_engine('sqlite+pysqlite:///declutter')
    Base.metadata.create_all(engine)


# Creates an engine and creates a SQLite3 database if it does not exist
# Returns the engine
def load_database():
    return create_engine('sqlite+pysqlite:///declutter')

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}', birth_date={self.birth_date}, date_of_death={self.date_of_death})>"

    def __str__(self):
        return f"{self.name} (Born: {self.birth_date}, Died: {self.date_of_death if self.date_of_death else 'N/A'})"

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.Integer, nullable = False)
    title = db.Column(db.String(100), nullable = False)
    publication_year = db.Column(db.Date, nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __str__(self):
        return f"{self.isbn} for title {self.title} is published in {self.publication_year} "



import os
from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from data_models import db, Author, Book

app = Flask(__name__)

# Ensure the 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')


MAIN_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = "./data"
DB_NAME = "library.sqlite"

# Get absolute path to the database file
DB_PATH = os.path.join(MAIN_FOLDER_PATH, DB_PATH, DB_NAME)

# Use absolute path in the URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'

db.init_app(app)

@app.route('/add_author',  methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        # retrieve form data
        name = request.form['name']
        birth_date_str= request.form['birth_date']
        date_of_death_str= request.form['date_of_death']

        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
        date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date() if date_of_death_str else None

        # create new Author instance
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)

        # add new_author to database and commit the session
        db.session.add(new_author)
        db.session.commit()

        display_message = "Author Added Successfully"

        return render_template('add_author.html', display_message=display_message)

    # if 'GET'
    return render_template('add_author.html')


@app.route('/add_book',  methods=['GET', 'POST'])
def add_book():
    authors = Author.query.all()  # Fetch all authors from the database
    if request.method == 'POST':
        # retrieve form data
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year_str = request.form['publication_year']
        author_id = request.form['author_id']

        # Assuming publication_year is just a year (e.g., '2000'), we convert it to a date
        publication_year = datetime.strptime(publication_year_str, '%Y').date()

        # create new Book instance
        new_book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)

        # add new_author to database and commit the session
        db.session.add(new_book)
        db.session.commit()

        display_message = "Book Added Successfully"
        return render_template('add_book.html', display_message=display_message, authors=authors)

    # if 'GET'
    return render_template('add_book.html', authors=authors)


@app.route('/')
def home():
    # Query all books from the Book  and authors table
    books = Book.query.all()
    authors =Author.query.all()
    # Pass the books data to the template
    return render_template('home.html', books=books, authors=authors)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')  # Get the search term from the URL query parameters

    books = []
    authors = []
    search_query = query

    if query:
        # Check if the query is an author's name
        author = Author.query.filter(Author.name.ilike(f'%{query}%')).first()  # Find first author that matches

        if author:
            # If the author is found, fetch all books written by that author
            books = Book.query.filter(Book.author_id == author.id).all()
            authors = [author]  # Only return this author in the authors list
        else:
            # If no author is found, search for books by title
            books = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
            authors = []  # No authors to show in this case

    return render_template('search_results.html', books=books, authors=authors, search_query=search_query)


"""
with app.app_context():
  db.create_all()
"""
if __name__ == "__main__":
    app.run(debug=True)
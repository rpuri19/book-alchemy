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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/add_author',  methods=['GET', 'POST'])
def index():
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

        display_message = "Author added successfully"
        return render_template('add_author.html', display_message=display_message)

    # if 'GET'
    return render_template('add_author.html')

"""
with app.app_context():
  db.create_all()
"""
if __name__ == "__main__":
    app.run(debug=True)
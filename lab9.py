from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Вариант №8

app = Flask('Portfolio dictonary')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_author = db.Column(db.String(00), nullable=False)
    book_name = db.Column(db.String(300), nullable=False)

    def dict(self):
        return f'Book{self.id}. "{self.book_author}" : {self.book_name}'


@app.route('/')
def main():
    books = Book.query.all()
    return render_template('index1.html', books_list=books)


# Добавление
@app.route('/add', methods=['POST'])
def add_product():
    data = request.json
    book = Book(**data)
    db.session.add(book)
    db.session.commit()

    global books
    id_last = books[-1]['id']
    id_new = id_last + 1
    data['id'] = id_new
    books.append(data)
    return 'OK'

# Удаление
@app.route('/clear', methods=["POST"])
def clear_experience():
    Book.query.delete()
    db.session.commit()
    return 'Cleared successfully!'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

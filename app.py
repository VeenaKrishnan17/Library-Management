from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test123@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)



class book(db.Model):
    bookId=db.Column(db.Integer,primary_key=True)
    bookTitle=db.Column(db.String(200),nullable=False)
    bookAuthor=db.Column(db.String(500),nullable=False)
    bookCount=db.Column(db.Integer,nullable=False)
    transaction = db.relationship('transaction', backref='book', lazy=True)

    def __init__(self,bookTitle,bookAuthor,bookCount):
        self.bookTitle=bookTitle
        self.bookAuthor=bookAuthor
        self.bookCount=bookCount


class student(db.Model):
    sId=db.Column(db.Integer,primary_key=True)
    sName=db.Column(db.String(200),nullable=False)
    sEmailId=db.Column(db.String(500),nullable=False)
    sContactNo=db.Column(db.Integer,nullable=False,unique=True)
    transaction = db.relationship('transaction', backref='student', lazy=True)

    def __init__(self,sName,sEmailId,sContactNo):
        self.bookTsNameitle=sName
        self.sEmailId=sEmailId
        self.sContactNo=sContactNo

    def __repr__(self) -> str:
        return f"{self.sId} - {self.sName}"

class transaction(db.Model):
    book_id=db.Column(db.Integer,db.ForeignKey(book.bookId),primary_key=True)
    stu_id=db.Column(db.Integer,db.ForeignKey(student.sId),primary_key=True)
    date_of_issue=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    due_date=db.Column(db.DateTime,nullable=False)
    


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__=="__main__":
    app.run()

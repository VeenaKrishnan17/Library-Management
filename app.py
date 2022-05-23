
from enum import unique
from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test123@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


#book table
class book(db.Model):
    bookId=db.Column(db.Integer,primary_key=True)
    bookTitle=db.Column(db.String(200),nullable=False)
    bookAuthor=db.Column(db.String(500),nullable=False)
    bookCount=db.Column(db.Integer,nullable=False)
    transaction = db.relationship('transaction', backref='book', lazy=True)

    def __init__(self,bookId,bookTitle,bookAuthor,bookCount):
        self.bookId=bookId
        self.bookTitle=bookTitle
        self.bookAuthor=bookAuthor
        self.bookCount=bookCount


#student table
class student(db.Model):
    sId=db.Column(db.Integer,primary_key=True)
    sName=db.Column(db.String(200),nullable=False)
    sEmailId=db.Column(db.String(500),nullable=False)
    sContactNo=db.Column(db.Integer,nullable=False,unique=True)
    transaction = db.relationship('transaction', backref='student', lazy=True)

    def __init__(self,sName,sEmailId,sContactNo):
        self.sName=sName
        self.sEmailId=sEmailId
        self.sContactNo=sContactNo

    def __repr__(self) -> str:
        return f"{self.sId} - {self.sName}"


#transaction table
class transaction(db.Model):
    book_id=db.Column(db.Integer,db.ForeignKey(book.bookId),primary_key=True)
    stu_id=db.Column(db.Integer,db.ForeignKey(student.sId),primary_key=True)
    date_of_issue=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    due_date=db.Column(db.DateTime,nullable=False)
    

#for testing purposr
@app.route("/test",methods=['GET'])
def test():
    return {'test' : 'test'}


#Get mmethod
@app.route("/books",methods=['GET'])
def getBooks():
    allBooks=book.query.all()
    output=[]
    for books in allBooks:
        currBook = {}
        currBook['bookId']=books.bookId
        currBook['bookTitle']=books.bookTitle
        currBook['bookAuthor']=books.bookAuthor
        currBook['bookCount']=books.bookCount
        output.append(currBook)

    return jsonify(output)


#post method
@app.route("/books",methods=['POST'])
def postBooks():
    bookData=request.get_json()
    books = book( bookId=bookData['bookId'],bookTitle=bookData['bookTitle'], bookAuthor=bookData['bookAuthor'], bookCount=bookData['bookCount'])
    db.session.add(books)
    db.session.commit()
    return jsonify(bookData)



if __name__=="__main__":
    app.run(debug=True)

  

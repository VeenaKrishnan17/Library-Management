
from crypt import methods
from enum import unique
from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import select

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/library'
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

    def __init__(self,sId,sName,sEmailId,sContactNo):
        self.sId=sId
        self.sName=sName
        self.sEmailId=sEmailId
        self.sContactNo=sContactNo

    def __repr__(self) -> str:
        return f"{self.sId} - {self.sName}"


#transaction table
class transaction(db.Model):
    transaction_id=db.Column(db.Integer,primary_key=True)
    book_id=db.Column(db.Integer,db.ForeignKey(book.bookId))
    stu_id=db.Column(db.Integer,db.ForeignKey(student.sId),)
    date_of_issue=db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    due_date=db.Column(db.DateTime,nullable=False)
    

#for testing purposr
@app.route("/test",methods=['GET'])
def test():
    return {'test' : 'test'}


#Get method for books
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


#post method for books
@app.route("/books",methods=['POST'])
def postBooks():
    bookData=request.get_json()
    books = book( bookId=bookData['bookId'],bookTitle=bookData['bookTitle'], bookAuthor=bookData['bookAuthor'], bookCount=bookData['bookCount'])
    db.session.add(books)
    db.session.commit()
    return jsonify(bookData)

#Get method for students
@app.route("/students",methods=['GET'])
def getStudents():
    allStudents=student.query.all()
    output=[]
    for students in allStudents:
        currStudents = {}
        currStudents['sId']=students.sId
        currStudents['sName']=students.sName
        currStudents['sEmailId']=students.sEmailId
        currStudents['sContactNo']=students.sContactNo
        output.append(currStudents)
    return jsonify(output)

#post method for students
@app.route("/students",methods=['POST'])
def postStudents():
    studentData=request.get_json()
    students = student( sId=studentData['sId'],sName=studentData['sName'], sEmailId=studentData['sEmailId'], sContactNo=studentData['sContactNo'])
    db.session.add(students)
    db.session.commit()
    return jsonify(studentData)

#get books whose count greater than 0
@app.route("/booksCountGreaterZero",methods=['GET'])
def getBooksGreaterThanZero():
    booksGreaterThanZero= db.session.query(book).filter(book.bookCount > 0)
    output=[]
    for books in booksGreaterThanZero:
        currBook = {}
        currBook['bookId']=books.bookId
        currBook['bookTitle']=books.bookTitle
        currBook['bookAuthor']=books.bookAuthor
        currBook['bookCount']=books.bookCount
        output.append(currBook)
    return jsonify(output)


#get method for all transactions
@app.route("/transactions",methods=['GET'])
def getTransactions():
    allTransactions=transaction.query_all()
    output=[]
    for transactions in allTransactions:
        currTransactions={}
        # currTransactions['transaction_id']=transactions.transaction_id
        currTransactions['book_id']=transactions.book_id
        currTransactions['stu_id']=transactions.stu_id
        currTransactions['date_of_issue']=transactions.date_of_issue
        currTransactions['due_date']=transactions.due_date




if __name__=="__main__":
    app.run(debug=True)

  

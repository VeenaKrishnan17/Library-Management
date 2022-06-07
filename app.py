from enum import unique
from xmlrpc.client import DateTime
from click import echo
from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from psycopg2 import Date
from sqlalchemy import select
from sqlalchemy import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/library' 
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)




#book table
class book(db.Model):
    bookId=db.Column(db.Integer,primary_key=True)
    bookTitle=db.Column(db.String(200),nullable=False)
    bookAuthor=db.Column(db.String(500),nullable=False)
    bookCount=db.Column(db.Integer,nullable=False)
    transaction = db.relationship('transaction', backref='book', lazy=True)

    def __init__(self,bookTitle,bookAuthor,bookCount):
        # self.bookId=bookId
        self.bookTitle=bookTitle
        self.bookAuthor=bookAuthor
        self.bookCount=bookCount


#student table
class student(db.Model):
    sId=db.Column(db.Integer,primary_key=True)
    sName=db.Column(db.String(200),nullable=False)
    sEmailId=db.Column(db.String(500),nullable=False)
    sContactNo=db.Column(db.String(20),nullable=False,unique=True)
    ransaction = db.relationship('transaction', backref='student', lazy=True)

    def __init__(self,sName,sEmailId,sContactNo):
        # self.sId=sId
        self.sName=sName
        self.sEmailId=sEmailId
        self.sContactNo=sContactNo

    def __repr__(self) -> str:
        return f"{self.sId} - {self.sName}"


#transaction table
class transaction(db.Model):
    trans_id=db.Column(db.Integer,primary_key=True)
    book_id=db.Column(db.Integer,db.ForeignKey(book.bookId),primary_key=True)
    stud_id=db.Column(db.Integer,db.ForeignKey(student.sId),primary_key=True)
    Action=db.Column(db.String(40),nullable=True)
    date_of_issue=db.Column(db.Date,default=datetime.today(),nullable=False)
    due_date=db.Column(db.DateTime,nullable=False)

    def __init__(self,book_id,stud_id,Action,due_date):
        
        self.book_id=book_id
        self.stud_id=stud_id
        self.Action=Action
        self.due_date=due_date


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

#get single book
@app.route("/books/<bookId>",methods=['GET'])
def getBook():
    gbook=book.query.get(id)
    return jsonify(gbook)


#post method for books
@app.route("/books",methods=['POST'])
def postBooks():
    bookData=request.get_json()
    books = book(bookTitle=bookData['bookTitle'], bookAuthor=bookData['bookAuthor'], bookCount=bookData['bookCount'])
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
    students = student(sId=studentData['sId'], sName=studentData['sName'], sEmailId=studentData['sEmailId'], sContactNo=studentData['sContactNo'])
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

#Get method for trans
@app.route("/trans",methods=['GET'])
def getTrans():
    allTrans=transaction.query.all()
    output=[]
    for transactions in allTrans:
        currTrans = {}
        currTrans['trans_id']=transactions.trans_id
        currTrans['book_id']=transactions.book_id
        currTrans['stud_id']=transactions.stud_id
        currTrans['Action']=transactions.Action
        currTrans['date_of_issue']=transactions.date_of_issue
        currTrans['due_date']=transactions.due_date
        output.append(currTrans)

    return jsonify(output)



#post method for trans
@app.route("/trans",methods=['POST'])
def postTrans():
    TransData=request.get_json()
    transactions = transaction(book_id=TransData['book_id'], stud_id=TransData['stud_id'], Action=TransData['Action'],due_date=TransData['due_date'])
    db.session.add(transactions)
    db.session.commit()
    return jsonify(TransData)



#get the details of most read books
@app.route("/mostReadBooks",methods=['GET'])
def mostReadBooks():
    mostReadBooks= db.session.execute('select book_id,date_of_issue, COUNT (*)from transaction GROUP BY book_id,date_of_issue ORDER BY count desc;')
    output=[]
    for books in mostReadBooks:
        currBook = {}
        currBook['book_id']=books.book_id
        currBook['date_of_issue']=books.date_of_issue
        currBook['count']=books.count
        output.append(currBook)
    return jsonify(output)



if __name__=="__main__":
    app.run(debug=True)

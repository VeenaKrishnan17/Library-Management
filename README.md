# Library Management
Database - PostgreSql
Language - Python
Framework - Flask

Required Tables
books, students, transaction

books                        
  book id (primary key)
  book name
  author name 
  year 
  rating 
  count

Students 
  student id (primary key)
  student name
  email 
  phone (unique)

Transaction 
  book_id 
  student_id 
  date of issue 
  due_date 

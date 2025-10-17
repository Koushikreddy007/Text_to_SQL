import sqlite3

#connecting to the database
connection=sqlite3.connect('student.db')

#create a cursor object to insert record,create table,retrive
cursor=connection.cursor()

table_info="""
    Create table STUDENT(NAME VARCHAR(20),AGE INT,CLASS VARCHAR(50),SECTION VARCHAR(25),MARKS INT);
"""

cursor.execute(table_info)
cursor.execute("INSERT INTO STUDENT VALUES('John',15,'10th','A',85)")
cursor.execute("INSERT INTO STUDENT VALUES('Alice',14,'9th','B',90)")
cursor.execute("INSERT INTO STUDENT VALUES('Bob',16,'11th','A',78)")
cursor.execute("INSERT INTO STUDENT VALUES('Eve',15,'10th','C',88)")
cursor.execute("INSERT INTO STUDENT VALUES('Charlie',14,'9th','A',92)")
cursor.execute("INSERT INTO STUDENT VALUES('David',16,'11th','B',80)")
cursor.execute("INSERT INTO STUDENT VALUES('Fiona',15,'10th','B',87)")
cursor.execute("INSERT INTO STUDENT VALUES('Grace',14,'9th','C',91)")
cursor.execute("INSERT INTO STUDENT VALUES('Hannah',16,'11th','A',83)")

print("The Inserted records are:")

data=cursor.execute("SELECT * FROM STUDENT")

for row in data:
    print(row)

connection.commit()
connection.close()

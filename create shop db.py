import sqlite3

#create a database
db = sqlite3.connect('shop.db')
cur = db.cursor()

#create a inventory table which contains total amount of cars for each type

#cur.execute(""" CREATE TABLE Inventory (
#            Cartype text,
#            Quantity integer
#           )""")


db.commit()

cur.execute("INSERT INTO Inventory VALUES('HATCHBACK', 25)")
cur.execute("INSERT INTO Inventory VALUES('SEDAN', 15)")
cur.execute("INSERT INTO Inventory VALUES('SUV', 15)")

db.commit()

print(cur.fetchall())
import csv, os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

#Setting up the database
engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

def main():
    """
    Imports data from a csv file into the
    database books table
    """

    csvfile = open('books.csv')
    reader = csv.reader(csvfile)
    next(reader)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",{"isbn": isbn, "title":title, "author":author, "year":year})
    db.commit()

if __name__ == "__main__":
    main()

# Project 1 | Web Programming with Python and JavaScript

### Introduction

In this project I have built an application about books reviews. Users are able to register and log-in at the beginning. Then, they can explore more than 5000 books, searching by title, author, year or ISBN. By clicking in a specific book, they will get data related to the book's reviews (other users reviews, number of reviews, average rating from the app and GoodReadsApi). There they can leave their review for others to see.

### Database

For this application, I have developed a Database to manage Users, Books and Reviews. I used Heroku free postgres plan. The users table consists on a username and a password columns. The books table saves information about title, author, release year and ISBN. The reviews table save information like user id, book id, title, opinion and rating.

### import.py

This file loads the 5000 books into my database. It uses SQLAlchemy library to execute this operation.

### application.py

This is the Flask Application. It has the following routes:

1. index: is the main route that lists all the books. It uses lazy loading, it loads chunks of 30 books. By accesing this route, it verify if the user is already logged in the application using the Flask session module. If it's not the case, I will redirect to the signin route

2. signin: This route makes possible the user login. It verifies that the username and the passwords introduced are valid, and it will redirect to the index if everything is correct. If it's not the case it will throw an alet to user.

3. signup: In this route users can register their profile in our database by introducing an username and a password.

4. logout: This just eliminate the session and redirect to the signin route.

5. book: By passing this route an ISBN code, it will display to the user all the information about the specific book (title, author, ISBN, release year, average rating, average rating from GoodReadsAPI, number of reviews and every review other users have made to the book). Also, the users will be able to publish their personal reviews by introducing the rate, title and opinion for the book.

6. api: This route is the API. It receives the ISBN code of the book and it returns a json that looks like this:


```javascript
  {
    'title': book.title,
    'author': book.author,
    'year': book.year,
    'isbn': book.isbn,
    'review_count': n_reviews,
    'average_rating': rating
  }
```

### templates

Here are the differents jinja2 templates. They are

1. layout.html: The basic template for the rest of a our html files. It just include bootstrap in our files.
2. sign-in.html: The sign-in html file that displays the login form.
3. sign-up.html: The sign-up html file that displays the registration form.
4. books.html: A navbar for the application logo, search bar and the logout button. Lists all the books as cards.
5. book.html: Displays the same navbar as the books.html file, but it displays the specific information about the book and its reviews.

### static

Includes the assets folder which contain the application logo. Also, and not less important the styles.css file that gives the UI a much more modern and better looking style to the application.


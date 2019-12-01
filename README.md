# Project 1

Web Programming with Python and JavaScript


When the user run the flask, the index route directs user to the "index.html" page, where user can either login, if he/she already has an account, or could click register, from where he'll/she'll be redirected to "register.html" page.

User can register from "register.html" by filling the details, which will prompt him/her to either success/failure message.

After registration, user can login into their account which will generate a session for user and redirect them to a search page "home.html", from where, user can enter their search queries to search the book catalogue.

On entering search queries and pressing search button, user is redirected to the "books.html" page, which displays the search results.

User has an option to click review on a particular book of their choice, for further reading the information about the book or submit a review/rating of their own on the "review.html" page.

On submitting the review, user will get a success/failure prompts if any.

On clicking the "Log Out" button, which is present from the time a user has logged in on the top right corner, user will be logged out and redirected to the home page i.e. "index.html"



#API

Developers can also access the data available on this website through API in JSON form through the "ISBN" number of an book, if they have it.

TO access it use this URL : http://127.0.0.1:5000/api/ISBN

on entering, a JSON data of the type like:

{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}

will be obtained and can be used.
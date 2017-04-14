postcodez
========

Django web app to lookup and validate postcodes returning the ward and borough.

### Problem

Nobody likes manual data entry - let's automate!

For a list of UK postcodes we need to fetch the ward & borough. Rather than manually copying and pasting individual postcodes into a website and then copying the results back we will clean the data, stick the postcodes in a queue for a processing then return the results in a web page.

### Heroku (Free Plan)

* Allows max 10k rows in postgres
* Allows one web worker and one other worker (django & redis worker)
* Allows up to 25MB redis memory

### Solution

A simple/naive django web app - because of the 10k row limit we will just purge the database and queue when a new request is made. It us unlikely that more than one person will use the service at a time so this is not a problem.

#### Heroku Deployment
```
heroku login
git push heroku master
heroku run python manage.py migrate
```

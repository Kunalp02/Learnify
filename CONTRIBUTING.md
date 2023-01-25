# Contributing to Learnify

First off, thank you for considering contributing to Learnify. It's people like you that make the open-source community such a great place to learn, inspire, and create.

## How to Setup

Before contributing to Learnify, you will have to fork the repo. or you can just download the repo.

### System Requirements
All requirements are already mentioned in the requirements.txt. Just you need to install the requirements.txt.

`pip install -r requirements.txt`

You will have to add the following API key in order to run the application. Visit the respected website and generate an API key after that replace that in the project. All these APIs are free and safe to use.

[Youtube data API](https://developers.google.com/youtube/v3)\
[Courier Send API](https://www.courier.com/docs/guides/getting-started/python/)\
[Open AI API](https://openai.com/api/)

## Migrate the database
This will create all the tables in the database

## Run the Server
`python manage.py runserver` To run the application it by default run on 8000. If you want it to run on some other port just add the port no after runserver like `python manage.py runserver 8000`

## Create Superuser
`python manage.py createsuperuser`
this command will create a superuser. you can now visit the admin URL 'localhost:8000/admin' to access and manage all the data. It is an admin panel.

# You will to make changes and make a pull request to this repo. Once it is approved will be merged
Thanks!

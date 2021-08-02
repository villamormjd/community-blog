# Getting Started with Community BLog

This project is created from [Django](https://www.djangoproject.com/) and [Django Rest Framework](https://www.django-rest-framework.org/). You can use `Postman` to test the API Endpoints. Once logged in, a token will generate and you can use the Token as Header:
```
  key: Authorization
  value: Bearer {generated token}
```

### Setting up Project

In the project directory:

### Install, Create, and activate Virtual Environment
 ```
 pip install virtualenv
 virtualenv venv
 ./venv/Scripts/activate
 ```
 'venv' is you virtual environment name


### Install Django and other library
```
  pip install -r requirements.txt
```

### Perform the migration for database and models
```
python manage.py migrate
```

### Run the project on your local
```
python manage.py runserver
```
Open [http://localhost:8000](http://localhost:8000) to view it in the browser.


### Available  Endpoints
* User Endpoints
```
Signup - api/auth/signup/
Login - api/auth/login/
```

* Posts Endpoints
```
Retrieve All Posts - api/posts/
Retrieve and Update Single Post  - api/posts/<id>/
Delete Post - api/posts/delete/<id>/

Retrieve Post by Logged in User - api/me/posts/
```

* Comment Endpoints
```
Retrieve all comments on a post - api/post/<post_id>/comments/
Retrieve, Upate and Delete comment - api/post/<post_id>/comments/<comment_id>
```

* Token API
```
api/gettoken/
```

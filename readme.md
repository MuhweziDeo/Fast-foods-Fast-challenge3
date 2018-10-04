# Fast Foods Fast Challenge3
A Restaurant Food Delivery and ordering API



[![Build Status](https://travis-ci.org/MuhweziDeo/Fast-foods-Fast-challenge3.svg?branch=develop)](https://travis-ci.org/MuhweziDeo/Fast-foods-Fast-challenge3)

[![Coverage Status](https://coveralls.io/repos/github/MuhweziDeo/Fast-foods-Fast-challenge3/badge.svg?branch=develop)](https://coveralls.io/github/MuhweziDeo/Fast-foods-Fast-challenge3?branch=develop)

[![Maintainability](https://api.codeclimate.com/v1/badges/b5c09d42343e10ee8bc8/maintainability)](https://codeclimate.com/github/MuhweziDeo/Fast-foods-Fast-challenge3/maintainability)

# Project Repo
https://github.com/MuhweziDeo/Fast-foods-Fast-challenge3.git

# Live Demo Link and Documentation
https://fast-foods-api-main.herokuapp.com/

# Functionality
- Create user accounts that can signin in the app. 
- Place an order for food.
- Get list of orders.
- Get a specific order.
- Update the status of an order. 
- Get the menu.
- Add food option to the menu.
- View the order history  for a particular user.

# Dependencies Used
- Flask(python web framework )
- Flask_Restplus(flask framework for building APis)
- Pytest(Testing Framework)
- Flask-Jwt-extended(Json Web Token authentication library)
- Postgres(Database server)


# End Points 
EndPoint                            | Functionality
    ------------------------            | --------------------
    `POST /auth/signup `                     | `create a user account`
    `POST /auth/login `                     | `Verify a user and create access token`
    `POST /users/orders `                     | `Create an order`
    `GET /users/orders  `               | `Get orders of a particular user`
    `GET /orders/ `         | `Get all orders(Admin only)`
    `GET /orders/<orderId> `        | `Get a particular order by its orderId(Admin only)`
    `PUT /orders/<orderId>`       | `update order status of an order(Admin only)`
    `GET /menu`       | `view Meals on the menu`
    `POST /menu`       | `Add meal option(Admin only)`

# How to use
- Signing up,username,password and confirm password are expected in post data.
{
  "username": "string",
  "password": "string",
  "confirm": "string"
}.
password and confrim fields must match before an account is created

- Logging In, Users provide in a username and password which are verified if they
belong to any user in the database.
{
  "username": "string",
  "password": "string"
}

- create a meal option,only Admins can create a meal option by entering a meal name 
and price, by default meal_status is set to Available.
{
  "meal_name": "string",
  "price": 0
}

- create order, a user can create an order by passing a valid token,location,meal
and quantity of the meal they want.
{
  "location": "string",
  "quantity": 0,
  "meal": "string"
}

##  Running locally and Testing
1. Running Locally
- Clone project repository ` git clone https://github.com/MuhweziDeo/Fast-foods-Fast-challenge3.git`
- cd into project directory
- Install a virtual enviroment `virtualenv venv`
- Activate Enviroment `source venv/bin/activate`
- Checkout develop branch -`git checkout develop`
- Install dependencies `pip install -r requirements.txt`
- run server,open terminal and run `python run.py`

2. Testing
- cd into project directory 
- Set up enviroment  for testing using export APP_SETTINGS='testing'
- open terminal and run `py.test --cov`

# Break down of tests
- Test(test_db) Database CRUD operations.
Test all database operations
- Test(test_meals,test_orders,test_users) api endpoints.
Test all routes for the api



## Developed by
- Muhwezi Deo









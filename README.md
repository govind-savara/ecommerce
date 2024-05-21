# ecommerce
e-commerce platform backend system that handles relational and non-relational databases with a smart rules engine.

This project built using Django Rest framework for creating Restful APIs. We used MySQL and MongoDB databases for storing data.

## Technical information:
- Django - 4.1.13
- PyMySQL - 1.1.0
- djongo - 1.3.6

All the requirements are list in requirements.txt file

## Installation
1. Clone this repository
 ```
 $ git clone https://github.com/govind-savara/ecommerce.git
 $ cd ecommerce
 ```
2. Install all the dependencies using the requirements.txt file.
 ```
 pip install -r requirements.txt
 ```
3. Create a .env file (refer to the sample file .env.example available in the repository)
4. Create migrations and run migrate command for the database setup.
 ```
 python manage.py makemigrations
 python manage.py migrate
 ```
5. Use django commands to run the project
```
$ python manage.py runserver
```

## Features
1. Basic User auth APIs (singup, login and logout)
2. Product management APIs
3. Place Order for the products API
4. Product Review CRUD APIs
5. Rules engine will be added in the near future
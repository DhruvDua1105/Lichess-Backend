# FastAPI Chess Player Rating Backend

This repository contains a backend application built using FastAPI for retrieving chess player ratings and generating CSV reports of their rating history.

## Features
Top Classical Players: Endpoint to retrieve the top classical players' ratings.\
Rating History: Endpoint to fetch the rating history of a specific player.\
CSV Report Generation: Endpoint to generate a CSV report of the rating history of top classical players.\
Authentication: Login and signup endpoints with JWT token generation for authentication.

## Setup
Clone the repository:

### `git clone https://github.com/DhruvDua1105/Lichess-Backend.git`

## Install dependencies:

### `pip install -r requirements.txt`

## Set up environment variables:

MYSECRETKEY: Secret key for JWT token generation.\
MYALGORITHM: Algorithm for JWT token generation.

## PostgreSQL Setup
This repository uses PostgreSQL as the database management system. Follow the steps below to set up PostgreSQL and configure the application to use it:

## Install PostgreSQL
If you haven't already installed PostgreSQL, you can download and install it from the official website. Alternatively, you can use a package manager like apt on Ubuntu or brew on macOS.

## Create Database
After installing PostgreSQL, create a new database for the application. You can do this using the createdb command-line utility or a graphical tool like pgAdmin.

### `createdb mydatabase`

## Set Environment Variables
Set the database URL in the .env file. Replace username, password, hostname, port, and database_name with your PostgreSQL credentials and database name.

### `DB_URL=postgresql://username:password@hostname:port/database_name`

## Update SQLAlchemy Configuration 
Update the SQLAlchemy configuration to use the PostgreSQL database. Modify the create_engine function call in your database.py file to use the URL_DATABASE environment variable.\
Run the database.py file

## Start Application
With the PostgreSQL database configured and running, start your FastAPI application. It should now connect to the PostgreSQL database specified in the environment variables.

## Run the application:

### `uvicorn main:app --reload`

## Swagger Docs can be accessed at http://127.0.0.1:8000/docs

## Endpoints
/topClassical/: GET endpoint to retrieve the top classical players' ratings.\
/{username}/ratinghistory/: GET endpoint to fetch the rating history of a specific player.\
/players/rating-history-csv: GET endpoint to generate a CSV report of the rating history of top classical players.\
/login: POST endpoint for user login.\
/signup: POST endpoint for user signup.

## Technologies Used
FastAPI: Web framework for building APIs with Python.\
SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library.\
Pydantic: Data validation and settings management using Python type annotations.\
Passlib: Password hashing library.\
JWT: JSON Web Tokens for authentication.\
Requests: HTTP library for making requests.\
CSV: Module for reading and writing CSV files.\
uvicorn: ASGI server for running the FastAPI application.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

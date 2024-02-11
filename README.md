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

## Run the application:

### `uvicorn main:app --reload`

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

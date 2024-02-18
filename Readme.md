# Project Name

Authentication & Authorization - JWT

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [File Structure](#file-structure)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project focuses on implementing authentication and authorization 
functionalities using email and password for user sign-up and sign-in 
processes. Upon successful authentication, a JWT (JSON Web Token) is 
generated and returned to the client. The JWT is used for authorization, 
where it must be included in each request sent from the client to the 
service. The system validates the token, ensuring it has not expired and 
handles error scenarios with appropriate error codes. Additionally, the 
project includes mechanisms for token revocation and token refreshing, 
allowing clients to renew tokens before expiration.

## Features

- Sign up (creation of user) using email and password
- Sign in
    a. Authentication of user credentials
    b. A token is returned as response preferably JWT
- Authorization of token
    a. Mechanism of sending token along with a request from client to service
    b. Should check for expiry
    c. Error handling (proper error codes in each failure scenario)
- Revocation of token
    a. Mechanism of revoking a token from backend
- Mechanism to refresh a token
    a. Client should be able to renew the token before it expires

## Installation

- docker build -t authapp .
- docker run -d --name authcontainer -p 80:80 authapp

## Usage

Below are examples of how to interact with the API endpoints using `curl` commands.

### User Signup

```bash
curl -X 'POST' \
  'http://127.0.0.1:80/user/signup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "full_name": "Devpriya Shivani",
  "email": "dpshiv12@gmail.com",
  "username": "devpriyash",
  "password": "nopass"
}'
```

### User Signin

```bash
curl -X 'POST' \
  'http://127.0.0.1:80/user/signin' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "dpshiv12@gmail.com",
  "password": "nopass"
}'
```

### User Authorization

```bash
curl -X 'GET' \
  'http://127.0.0.1:80/user/protected' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRwc2hpdjEyQGdtYWlsLmNvbSIsImV4cCI6MTcwODM2NDMxOH0.nmOUjKEmLfC-F6JCTeFJpqLp1DuntYuYKGVRWOSLkzM'
```

### Token Revocation

```bash
curl -X 'POST' \
  'http://127.0.0.1:80/user/revoke-token/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRwc2hpdjEyQGdtYWlsLmNvbSIsImV4cCI6MTcwODM2NDMxOH0.nmOUjKEmLfC-F6JCTeFJpqLp1DuntYuYKGVRWOSLkzM"
}'
```


### Refresh Token

```bash
still in progress
```

## File Structure

AP/
│
├── apenv/
|   └── ...
├── app/
│   └── auth/
|       └── model.py
|       └── router.py
|       └── utils.py
├── file_store/
│   └── user.json
├── .env
├── main.py
├── requirements.txt
└── README.md


## Endpoints

Detailed descriptions of each API endpoint, including their URLs, methods, 
request bodies (if applicable), authorization requirements, and response 
formats.

### Endpoint: User Signup

- **URL**: `http://localhost:80/user/signup/`
- **Method**: `POST`
- **Description**: Handles user signup by adding the user data to the 
  `users.json` file and returning a JWT token upon successful creation. 
  :param user: UserSchema - the user data to be signed up 
  :return: dict - a dictionary containing the JWT token
- **Request Body**: 
```json
{
    "full_name": "Devpriya Shivani",
    "email": "dpshiv12@gmail.com",
    "username": "devpriyash",
    "password": "nopass"
}
```
- **Response Body**: 
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRwc2hpdjEyQGdtYWlsLmNvbSIsImV4cCI6MTcwODI1OTE1N30.RF7g3IoBuwy0SeHSmGxZHoHUttz0b2UVZjkfSheyCl4"
}
```

### Endpoint: User Signin

- **URL**: `http://localhost:80/user/signin/`
- **Method**: `POST`
- **Description**: Handles user login by checking if the provided credentials 
  are valid. 
  :param user: UserLoginSchema - the user credentials 
  :return: dict - a dictionary containing the JWT token
- **Request Body**: 
```json
{
  "email": "dpshiv12@gmail.com",
  "password": "nopass"
}
```
- **Response Body**: 
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRwc2hpdjEyQGdtYWlsLmNvbSIsImV4cCI6MTcwODI1OTM2OH0.Vy43NEb9qCFVx_9XSGKGlytayjMxLcmOB3XefEOzMFo"
}
```

### Endpoint: User Authorization

- **URL**: `http://localhost:80/user/protected/`
- **Method**: `GET`
- **Description**: A protected route that requires a valid JWT token to 
  access it. :param payload: dict - the JWT token payload 
  :return: dict - a dictionary containing the message and user data
- **Request Body**: 
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Imtha3VsQGhvbWUuaW4iLCJleHAiOjE3MDgyNDA4NDV9.R00KDmpJGYtlj9OddvenRFWAXaLNAlhIkoGkreuvfyY"
}
```
- **Response Body**: 
```json
{
  "message":"This is a protected route",
  "user":{"email":"dpshiv12@gmail.com","exp":1708259368}
}
```

### Endpoint: Token Revocation

- **URL**: `http://127.0.0.1:80/user/revoke-token/`
- **Method**: `POST`
- **Description**: Revoke a token. :param token: Token - the JWT token 
  :return: dict - a dictionary containing the access token
- **Request Body**: 
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Imtha3VsQGhvbWUuaW4iLCJleHAiOjE3MDgyNDA4NDV9.R00KDmpJGYtlj9OddvenRFWAXaLNAlhIkoGkreuvfyY"
}
```
- **Response Body**: 
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Imtha3VsQGhvbWUuaW4iLCJleHAiOjE3MDgyNDA4NDV9.R00KDmpJGYtlj9OddvenRFWAXaLNAlhIkoGkreuvfyY"
}
```

### Endpoint: Refresh Token
- **URL**: `http://127.0.0.1:80/user/refresh-token/`
- **Method**: `POST`
- **Description**: Endpoint to refresh an expired token. 
  :param request: OAuth2PasswordRequestForm - form containing the refresh token 
  :return: dict - a dictionary containing the new access token
- **Request Body**: 
  WIP
- **Response Body**: 
  WIP

## Security

### Authentication

This API uses JSON Web Tokens (JWT) for authentication. Upon successful login 
or signup, the user receives a JWT token which is then included in the 
Authorization header for accessing protected routes.

### Authorization

Protected routes require a valid JWT token to access. If the token is missing, 
expired, or invalid, the API returns a 401 Unauthorized error.

### Token Revocation

Users can revoke their tokens by logging out, which invalidates the token on 
the server side. Additionally, tokens can be programmatically revoked using 
the `/user/revoke-token/` endpoint.

### Token Refresh

Expired tokens can be refreshed using the `/user/refresh-token/` endpoint. 
This endpoint requires a valid refresh token, which is exchanged for a new 
access token.

### HTTPS

For enhanced security, it's recommended to deploy this API over HTTPS to 
encrypt data transmitted between the client and server.

## Contributing

Contributions are welcome and appreciated! If you'd like to contribute to 
this project, please follow these guidelines:

1. **Fork** the repository on GitHub.
2. **Clone** your forked repository to your local machine.
3. **Create a new branch** from the `main` branch for your changes.
4. Make your desired changes and ensure that the code passes any existing 
  tests.
5. Add tests for your changes if applicable.
6. Run the tests to ensure they pass.
7. **Commit** your changes with descriptive commit messages.
8. **Push** your changes to your forked repository.
9. Submit a **pull request** to the `main` branch of the original repository.

### Contribution Guidelines

- Before starting work on an issue, please **comment** on the issue to let 
  others know you're working on it.
- Follow the **coding style** and **conventions** used in the project.
- Write **clear and descriptive** commit messages.
- Ensure any **new code is well-tested** to maintain code quality.
- Keep the **scope of changes** in your pull request as small as possible.

Thank you for your interest in contributing to this project!

## License

This project is licensed under the [MIT License](LICENSE).

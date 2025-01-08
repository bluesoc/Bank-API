# Bank-API
RESTFul Bank API, with transaction logging and authentication system.

⚠️ In Development 🌶️

### Tech Stack

* Flask
* Flask JWT
* Flask RESTful

### API Routes

| Method | Endpoint        | Description                                      |
|--------|------------------|--------------------------------------------------|
| POST   | /register        | Registers a new user.                            |
| POST   | /login           | Authenticates a user and generates a JWT token. |
| POST   | /accounts        | Creates a new account associated with the user. |
| GET    | /accounts        | Returns the account information of the authenticated user. |

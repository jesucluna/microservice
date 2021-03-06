# Author
- Jesus Caraballo

# Requirements
- Python
- Flask
- MySQL
- Docker

# Simple Development Guide
## Before to start
```sh
  # Clone
  $ git clone https://github.com/jesucluna/microservice.git
  $ cd microservice
```

## Docker instructions
### 1. Run and update
```sh
  # Create an image and container with compose
  $ docker-compose up --build
```   


# Simple Change log
## [1.0.0]
- Minimalist application.
- Detailed `readme`.
- Common `.gitignore` flask file.
- Initial `Dockerfile`.
- `docker-compose.yml` for make container web; redis and mysql database.
- You can save into databases, timestamp and temperature, current values from Cartagena Colombia.

## [1.1.0]
- You can save directly into databases for '/api/get'.
- `app.py` updated.

## [1.1.1]
- You can save directly into databases for '/api/post'.
- `app.py` updated.
- Readability in code improved.

## [1.1.2]
- `docker-compose.yml` updated for connect to db
- `app.py` updated.

## [1.1.3]
- `docker-compose.yml` updated for connect to mysqldb to port 80

## [1.2.0]
- `index.html` updated
- `home.html` updated
- `main.html` updated

## [1.2.1]
- You can get data inside json directly from databases for '/api/get'.
- `app.py` updated


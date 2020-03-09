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
- You can save directly into databases for '192.168.99.100/api/get'.
- `app.py` updated.

## [1.1.1]
- You can save directly into databases for '192.168.99.100/api/post'.
- `app.py` updated.
- Readability in code improved.
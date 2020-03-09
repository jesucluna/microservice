FROM python:3.6-buster

#Install all extensions
RUN pip install Flask
RUN pip install flask-mysqldb
RUN pip install redis
RUN pip install pytz

# Create folders 
RUN mkdir static
RUN mkdir static/css
RUN mkdir static/js
RUN mkdir templates

# Export (copy option) from Project to Docker container
COPY static/css/styles.css  static/css
COPY static/js/main.js static/js
COPY templates/* templates/
COPY app.py / 


ENV FLASK_ENV="development"
ENV FLASK_APP="app.py"

CMD flask run --host 0.0.0.0
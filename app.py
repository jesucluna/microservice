from flask import Flask, render_template, request, flash, redirect, url_for,jsonify
from flask_mysqldb import MySQL
import redis
from pytz import timezone
from datetime import datetime
import urllib.request, json

app = Flask(__name__)

#Mysql and Redis connection 
app.config['MYSQL_HOST']='db'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='microservice'
mysql = MySQL(app)
r_server = redis.Redis("redis")

#settings
app.secret_key = 'mysecretkey'

#Principal route for human client
@app.route('/')
def index():
    cur=mysql.connection.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS `microservice` (`ID` INT NOT NULL AUTO_INCREMENT, `timestamp` TIMESTAMP NOT NULL,`temperature` FLOAT NOT NULL ,PRIMARY KEY (`id`))')
    cur.execute('SELECT * FROM microservice')
    data=cur.fetchall()
    y = iotjson()
    date,temperature = adapjtodata(y)
    return render_template('index.html', data=data, date=date,temperature=temperature)

#route for save data into db with a post method trhough html view and api's value of temperature
@app.route('/microserv/<string:temperature>', methods=['POST'])
def add_microserv(temperature):
    if request.method == 'POST':
        date = gettime()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO microservice (timestamp, temperature) VALUES (%s,%s)',(date,temperature))
        mysql.connection.commit()
        cur.close()
        if r_server.set("timestamp",date):
          flash('Data Added Successfully')
        
        return redirect(url_for('index'))

#route for save data into db with a post method trough html view and human client
@app.route('/microserv', methods=['POST'])
def add_micro():
    if request.method == 'POST':
        timestamp = request.form['timestamp']
        temperature = request.form['temperature']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO microservice (timestamp, temperature) VALUES (%s,%s)',(timestamp,temperature))
        mysql.connection.commit()
        cur.close()
        r1= r_server.set("timestamp",timestamp)
        r2= r_server.set("temperature",temperature)
        if r1 and r2:
          flash('Data Added Successfully')
        return redirect(url_for('index'))
#route for delete a data from database, through url you can pass id to delete
@app.route('/delete/<string:id>')
def delete(id):
    cur= mysql.connection.cursor()
    cur.execute('DELETE FROM microservice WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Data with id {0}'.format(id)+' Removed Successfully')
    return redirect(url_for('index'))

# /index for show design pattern used
@app.route('/index')
def home():
    return render_template('home.html')

# /api/post for save directly into databases, no human client
@app.route('/api/post')
def postiot():
    date = gettime()
    temperature = gettemp()
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO microservice (timestamp, temperature) VALUES (%s,%s)',(date,temperature))
    mysql.connection.commit()
    cur.close()
    if r_server.set("timestamp",date):
        flash('Data Added Successfully from IOT directly')
    return redirect(url_for('index'))

# /api/get for get json from database, no human client
@app.route('/api/get')
def getiot():
    cur=mysql.connection.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS `microservice` (`ID` INT NOT NULL AUTO_INCREMENT, `timestamp` TIMESTAMP NOT NULL,`temperature` FLOAT NOT NULL ,PRIMARY KEY (`id`))')
    cur.execute('SELECT * FROM microservice')
    data=cur.fetchall()
    if data:
        return jsonify(data)
    else:
        return jsonify(error='Database is empty... Please fill it')

#Get datetime
def gettime():
    colombia = timezone('America/Bogota')
    c_time = datetime.now(colombia)
    return (c_time.strftime("%Y-%m-%d %T"))

#Get Cartagena's temperature from Api
def gettemp():
    with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?id=3687238&appid=ccd94a61a3605281b41a9e213664685a") as url:
        data = json.loads(url.read().decode())
        return(data["main"]["temp"]-273.15)

#Save timedate and temperature inside a Json
def iotjson():
    d = gettime()
    t = gettemp()
    y =  ('{ "timestamp":"%s", "temperature":"%s"}') % (d,t)
    return json.loads(y)

#Adapter for extract data from Json
def adapjtodata(y):
    date= y["timestamp"]
    tempe= y["temperature"]
    return(date,tempe)

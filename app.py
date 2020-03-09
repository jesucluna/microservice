from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL
import redis
from pytz import timezone
from datetime import datetime
import urllib.request, json

app = Flask(__name__)

#Mysql and Redis connection 
app.config['MYSQL_HOST']='192.168.99.100'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='microservice'
mysql = MySQL(app)
r_server = redis.Redis("192.168.99.100")

#settings
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cur=mysql.connection.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS `microservice` (`ID` INT NOT NULL AUTO_INCREMENT, `timestamp` TIMESTAMP NOT NULL,`temperature` FLOAT NOT NULL ,PRIMARY KEY (`id`))')
    cur.execute('SELECT * FROM microservice')
    data=cur.fetchall()
    y = iotjson()
    date,temperature = adapjtodata(y)
    return render_template('index.html', data=data, date=date,temperature=temperature)


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


@app.route('/delete/<string:id>')
def delete(id):
    cur= mysql.connection.cursor()
    cur.execute('DELETE FROM microservice WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Data with id {0}'.format(id)+' Removed Successfully')
    return redirect(url_for('index'))

 
def gettime():
    colombia = timezone('America/Bogota')
    c_time = datetime.now(colombia)
    return (c_time.strftime('%D %T'))

def gettemp():
    with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?id=3687238&appid=ccd94a61a3605281b41a9e213664685a") as url:
        data = json.loads(url.read().decode())
        return(data["main"]["temp"]-273.15)

def iotjson():
    d = gettime()
    t = gettemp()
    y =  ('{ "timestamp":"%s", "temperature":"%s"}') % (d,t)
    return json.loads(y)

def adapjtodata(y):
    date= y["timestamp"]
    tempe= y["temperature"]
    return(date,tempe)

from flask import Flask,render_template,request,redirect
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml

form = Flask(__name__)
Bootstrap(form)
#Configure database
db = yaml.load(open('db.yaml'))
form.config['MYSQL_HOST'] = db['mysql_host']
form.config['MYSQL_USER'] = db['mysql_user']
form.config['MYSQL_PASSWORD'] = db['mysql_password']
form.config['MYSQL_DB'] = db['mysql_db']
form.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(form)

@form.route('/',methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        form = request.form
        name = form['name']
        age = form['age']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO employee VALUES(%s,%s)',(name,age))
        mysql.connection.commit()
    return render_template('index.html')

@form.route('/employees')
def employee():
    cur = mysql.connection.cursor()
    result_value = cur.execute('SELECT * FROM employee')
    if result_value >0:
        employees = cur.fetchall()
        return render_template('employees.html',employees = employees)
if __name__ == '__main__':
    form.run(debug='True')

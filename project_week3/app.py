from flask import Flask, render_template, request, jsonify
from flaskext.mysql import MySQL
import hashlib

app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_DATABASE_USER'] = 'truong'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'soap_3'
app.config['MYSQL_DATABASE_HOST'] = 'localhost:3306'


@app.route('/')
def hello_world():
    return render_template("layout/login.html")


@app.route('/signup')
def sign_up():
    return render_template("layout/signup.html")


@app.route('/api/signup', methods=['POST'])
def new_user():
    conn = mysql.connect()
    cursor = conn.cursor()
    pass_sha512 = hashlib.sha512(request.json['password'].encode('utf-8')).hexdigest();
    cursor.execute("INSERT INTO `users`(`email`, `password`) VALUES ('{}','{}')".format(request.json['email'], pass_sha512))
    conn.commit()
    return jsonify(request.json)


if __name__ == '__main__':
    app.run()
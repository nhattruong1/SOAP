from flask import Flask, render_template, request, jsonify
from flaskext.mysql import MySQL
import hashlib
import random
import pymysql

app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_DATABASE_USER'] = 'truong'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'soap_3'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

@app.route('/')
def hello_world():
    return render_template("layout/login.html")


@app.route('/signup')
def sign_up():
    return render_template("layout/signup.html")

@app.route('/get-otp', methods=['POST'])
def get_otp():
    json_req = request.json
    email = json_req['email']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    otp = random.randint(1000, 9999)
    cursor.execute("SELECT * FROM `users` WHERE `email` = '{}'".format(email))
    check_valid_user = cursor.fetchmany()
    return jsonify(check_valid_user)

    # cursor.execute("INSERT INTO `users_otp`(`user_id`, `code`, `time_expired`) VALUES ('{}','{}',now() + INTERVAL 5 MINUTE)".format(1,otp))



@app.route('/api/signup', methods=['POST'])
def new_user():
    json_req = request.json
    email = json_req['email']
    password = json_req['password']
    conn = mysql.connect()
    cursor = conn.cursor()
    pass_sha512 = hashlib.sha512(password.encode('utf-8')).hexdigest()
    check_email = cursor.execute("SELECT * FROM `users` WHERE `email` = '{}'".format(email))
    if check_email < 1:
        cursor.execute("INSERT INTO `users`(`email`, `password`) VALUES ('{}','{}')".format(email, pass_sha512))
        conn.commit()
        message = {
            'status': 200,
            'message': 'User added successfully!',
        }
        response = jsonify(message)
        response.status_code = 200
        return response
    else:
        return not_found()


if __name__ == '__main__':
    app.run()
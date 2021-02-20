from flask import Flask, render_template, request, jsonify, session, redirect
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)
app.secret_key = "abc"
mysql = MySQL(app)
app.config['MYSQL_DATABASE_USER'] = 'truong'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'soap_week5'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306

admin_id = 'root'
admin_username = 'root'
admin_password = 'root'
admin_permission = 1  # 1 is teacher, 0 is student

def not_found():
    message = {
        'status': 404,
        'message': 'Something wrong',
    }
    response = jsonify(message)
    response.status_code = 404
    return response

@app.route('/')
def home():
    if 'admin_id' in session:
        session.pop('admin_id', None)
    if 'user_id' in session:
        return render_template('home.html',data = session)
    else:
        return redirect('/login')

@app.route('/login')
def login():
    if 'admin_id' in session:
        session.pop('admin_id', None)
    if 'user_id' in session:
        return redirect('/')
    else:
        return render_template('login.html')

@app.route('/subjects')
def subjects():
    if 'admin_id' in session:
        session.pop('admin_id', None)
    if 'user_id' in session:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT soap_subjects.name as subject_name,soap_admin.name as teacher FROM `soap_subjects` join `soap_admin` on `soap_admin`.`id` = `soap_subjects`.`teacher_id`")
        conn.commit()
        list_subject = cursor.fetchall()
        return render_template('subjects.html',data = list_subject)
    else:
        return redirect('/')

@app.route('/history')
def history_assignment():
    if 'admin_id' in session:
        session.pop('admin_id', None)
    if session:
        return render_template('history_assignment.html')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    if 'admin_id' in session:
        session.clear()
        return redirect('/admin')
    elif 'user_id' in session:
        session.clear()
        return redirect('/')

@app.route('/auth-login', methods=['POST'])
def auth_login():
    json_req = request.json
    username = json_req['username']
    password = json_req['password']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `soap_users` WHERE `username` = '{}' and `password` = '{}'".format(username,password))
    conn.commit()
    account = cursor.fetchone()
    if account:
        session['user_id'] = account['id']
        session['username'] = account['username']
        session['name'] = account['name']
        session['user_type'] = account['type']
        message = {
            'status': 200,
            'message': 'login success!'
        }
        response = jsonify(message)
        response.status_code = 200
        return response
    else:
        return not_found()

@app.route('/auth-login-admin', methods=['POST'])
def auth_login_admin():
    json_req = request.json
    username = json_req['username']
    password = json_req['password']
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM `soap_admin` WHERE `username` = '{}' and `password` = '{}'".format(username,password))
    conn.commit()
    account = cursor.fetchone()
    if account:
        session['admin_id'] = account['id']
        session['admin_username'] = account['username']
        session['admin_name'] = account['name']
        message = {
            'status': 200,
            'message': 'login success!'
        }
        response = jsonify(message)
        response.status_code = 200
        return response
    else:
        return not_found()

@app.route('/admin')
def admin_home():
    if 'user_id' in session:
        session.pop('user_id', None)
    if 'admin_id' in session:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT soap_subjects.name as subject_name,soap_admin.name as teacher,soap_subjects.id FROM `soap_subjects` join `soap_admin` on `soap_admin`.`id` = `soap_subjects`.`teacher_id` where soap_admin.id = '{}'".format(session['admin_id']))
        conn.commit()
        list_subject = cursor.fetchall()
        return render_template('admin.html',data = session,subject = list_subject)
    else:
        return redirect('/admin-login')

@app.route('/admin-login')
def admin_login():
    if 'user_id' in session:
        session.pop('user_id', None)
    if 'admin_id' in session:
        return redirect('/admin')
    else:
        return render_template('admin_login.html')

@app.route('/api/add-quizz',methods=['POST'])
def add_quizz():
    json_req = request.json
    subject_id = json_req['subject_id']
    quizz_name = json_req['name']
    arr_question = json_req['array_question']

    connect = mysql.connect()
    cursorr = connect.cursor(pymysql.cursors.DictCursor)
    cursorr.execute("INSERT INTO `soap_quizz`(`content`, `subject_id`,`time`) VALUES ('{}','{}','{}')".format(quizz_name, subject_id,60))
    id_quizz = cursorr.lastrowid
    connect.commit()
    for question in arr_question:
        add_question(id_quizz,question)
    message = {
        'status': 200,
        'message': 'success!'
    }
    response = jsonify(message)
    response.status_code = 200
    return response

def add_question(id_quizz,question):
    connect = mysql.connect()
    cursorr = connect.cursor(pymysql.cursors.DictCursor)
    cursorr.execute("INSERT INTO `soap_question`(`quizz_id`, `content`) VALUES ('{}','{}')".format(id_quizz,question["name"]))
    id_question = cursorr.lastrowid
    connect.commit()
    for answer in question["answer"]:
        add_answer(id_question,answer)
    return id_quizz

def add_answer(id_question,answer):
    connect = mysql.connect()
    cursorr = connect.cursor(pymysql.cursors.DictCursor)
    cursorr.execute("INSERT INTO `soap_answer`(`question_id`, `content`,`is_correct`) VALUES ('{}','{}','{}')".format(id_question,answer["content"], answer["correct"] == "true" and 1 or 0))
    connect.commit()
    return 1

if __name__ == '__main__':
    app.run(debug=True)

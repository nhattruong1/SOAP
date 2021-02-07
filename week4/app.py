from flask import Flask, render_template, request, jsonify, session,redirect

app = Flask(__name__)
app.secret_key = "abc"

admin_id = 'root'
admin_username = 'root'
admin_password = 'root'
admin_permission = 1  # 1 is teacher, 0 is student

@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/auth_login')
def auth_login():
    return 

if __name__ == '__main__':
    app.run(debug=True)

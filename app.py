from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import re

app = Flask(__name__)
app.secret_key = 'ys124126'

db = pymysql.connect(host="localhost", user="root", password="ys124126", database="recorvery_system", charset="utf8")
cursor = db.cursor()


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']
        depart = request.form['depart']
        cursor.execute('select * from user where email=%s and password=%s and rol=%s and depart=%s',
                       (email, password, rol, depart))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user[0]
            session['name'] = user[1]
            session['email'] = user[2]
            session['role'] = user[4]
            session['depart'] = user[5]
            mesage = 'logged in successfully'
            return render_template('check.html', mesage=mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage=mesage)


# 注销功能
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']
        rol = request.form['rol']
        depart = request.form['depart']
        cursor.execute('select * from user where email=%s and password=%s and rol=%s and depart=%s',
                       (email, password, rol, depart))
        account = cursor.fetchone()
        if account:
            mesage = '账户已存在 !'
        #     检查是否符合邮箱格式
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = '邮箱格式错误!'
        elif not username or not password or not email:
            mesage = '请全部填写!'
        else:
            id = 0
            cursor.execute('insert into user values (%s,%s,%s,%s,%s,%s)', (id, username, email, password, rol, depart))
            db.commit()
            mesage = '注册成功!'
    elif request.method == 'POST':
        mesage = '请全部填写 !'
    return render_template('register.html', mesage=mesage)


@app.route('/check')
def check():
    return render_template('check.html')


@app.route('/flush', methods=['POST', 'GET'])
def flush():
    cursor.execute('select * from patient_info')
    result = cursor.fetchall()
    # for items in result:
    #     print(items)
    #     for item in items:
    #         print(item)
    return render_template('check.html', data=result)


@app.route('/add_patient', methods=['POST', 'GET'])
def add_patient():
    mesage = ''
    if request.method == 'POST' and 'patient_name' in request.form and 'age' in request.form and 'patient_id' in request.form:
        patient_name = request.form['patient_name']
        sex = request.form['sex']
        age = request.form['age']
        patient_id = request.form['patient_id']
        start_time = request.form['start_time']
        diagnosis_time = request.form['diagnosis_time']
        cursor.execute('select * from patient_info where patient_name=%s and sex=%s and age=%s and patient_id=%s',
                       (patient_name, sex, age, patient_id))
        account = cursor.fetchone()
        if account:
            mesage = '患者已存在 !'
        elif not patient_name or not age or not patient_id:
            mesage = '请全部填写!'
        else:
            cursor.execute('insert into patient_info values (%s,%s,%s,%s,%s,%s,%s,%s)',
                           (patient_id, patient_name, sex, age, None, start_time, diagnosis_time, None))
            db.commit()
            mesage = '增加成功!'
    elif request.method == 'POST':
        mesage = '请全部填写 !'
    return render_template('add_patient.html', mesage=mesage)


if __name__ == '__main__':
    app.run(debug=True)

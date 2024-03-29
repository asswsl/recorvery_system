from flask import Flask, render_template, request, redirect, url_for, session
import re
from sql import cursor, db
from datetime import date
from admin import admin_blue
from nurse import nurse_blue

app = Flask(__name__)
app.secret_key = 'mgm81849117415'

app.register_blueprint(admin_blue, url_prefix='/admin')
app.register_blueprint(nurse_blue, url_prefix='/nurse')


@app.route('/')
def index():
    return render_template('login.html')


# 登陆
@app.route('/login', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']  # 邮箱
        password = request.form['password']  # 密码
        rol = request.form['rol']  # 角色
        depart = request.form['depart']  # 部门
        cursor.execute('select * from user where email=%s and password=%s and rol=%s and depart=%s',
                       (email, password, rol, depart))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user[0]
            session['name'] = user[1]
            session['email'] = user[2]
            session['rol'] = user[4]
            session['depart'] = user[5]
            mesage = 'logged in successfully'
            # 根据角色不同，进入不同的页面
            if session['rol'] == '护士站':
                # 当进入护士站页面时，同步显示出登记病人信息以及治疗项目信息
                cursor.execute('select * from patient_info')
                result = cursor.fetchall()
                cursor.execute('select * from treat_info')
                check_result = cursor.fetchall()
                return render_template('nurse.html', mesage=mesage, data=result, check_data=check_result)
            elif session['rol'] == '管理员':
                return render_template('admin.html', mesage=mesage)
            elif session['rol'] == '医生站':
                return render_template('doctor.html')
            else:
                return render_template('user.html')
        else:
            mesage = '请输入准确信息!'
    return render_template('login.html', mesage=mesage)


# 注册
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


# 注销功能
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

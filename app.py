from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import re

app = Flask(__name__)
app.secret_key = 'mgm81849117415'

db = pymysql.connect(host="localhost", user="root", password="ys124126", database="recorvery_system", charset="utf8")
cursor = db.cursor()


@app.route('/')
def index():
    return render_template('login.html')


# 登陆
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
            cursor.execute('select * from patient_info')
            result = cursor.fetchall()
            # 根据角色不同，进入不同的页面
            if session['role'] == '护士站':
                return render_template('check.html', mesage=mesage, data=result)
            else:
                return render_template('user.html')
        else:
            mesage = '请输入准确信息!'
    return render_template('login.html', mesage=mesage)


# 注销功能
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))


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


# 护士站首页
@app.route('/check')
def check():
    cursor.execute('select * from patient_info')
    result = cursor.fetchall()
    cursor.execute('select * from patient_info where hospital_id is not null')
    check_result = cursor.fetchall()
    return render_template('check.html', data=result,check_data=check_result)


# 刷新
@app.route('/flush', methods=['POST', 'GET'])
def flush():
    cursor.execute('select * from patient_info')
    result = cursor.fetchall()
    cursor.execute('select * from patient_info where hospital_id is not null')
    check_result = cursor.fetchall()
    # print(check_result)
    return render_template('check.html', data=result, check_data=check_result)


# 增加患者信息
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
        cursor.execute('select * from patient_info where patient_id=%s', patient_id)
        id = cursor.fetchone()
        if account:
            mesage = '患者已存在 !'
        elif id:
            mesage = '患者卡号不能相同'
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


# 搜索患者信息
@app.route('/search_patient', methods=['POST', 'GET'])
def search_patient():
    mesage = ''
    result = ''
    fields = ['patient_id', 'patient_name', 'sex', 'age', 'start_time', 'diagnosis_time']
    if request.method == 'POST' and 'data' in request.form and 'kind' in request.form:
        kind = request.form['kind']
        data = request.form['data']
        if kind not in fields:
            mesage = '错误查询'
        elif not data:
            mesage = '请填写查询数据'
        else:
            cursor.execute('select * from patient_info where %s=%%s' % kind, (data,))
            result = cursor.fetchall()
            if not result:
                mesage = '不存在信息'
            else:
                mesage = '查询成功'
            print(result)
    return render_template('search_patient.html', data=result, mesage=mesage)


# 删除患者信息
@app.route('/delete_patient', methods=['POST', 'GET'])
def delete_patient():
    mesage = ''
    cursor.execute('select * from patient_info')
    result = cursor.fetchall()
    if request.method == 'POST' and 'id' in request.form:
        del_id = request.form['id']
        cursor.execute('delete from patient_info where patient_id=%s', del_id)
        db.commit()
        # 点击后刷新表格
        cursor.execute('select * from patient_info')
        result = cursor.fetchall()
        # resu = cursor.execute('select * from patient_info where patient_id=%s', del_id)
        if not result:
            mesage = '删除成功'
        else:
            mesage = '删除失败'
    return render_template('delete_patient.html', data=result, mesage=mesage)


# 修改患者信息
@app.route('/alter_patient', methods=['POST', 'GET'])
def alter_patient():
    mesage1 = ''
    mesage2 = ''
    result = ''
    if request.method == 'POST' and 'patient_id' in request.form:
        patient_id = request.form['patient_id']
        cursor.execute('select * from patient_info where patient_id=%s', (patient_id))
        result = cursor.fetchone()
        print(result)
        if not result:
            mesage1 = '查询失败'
        else:
            mesage1 = '查询成功'
    if request.method == 'POST' and 'patient_name' in request.form and 'sex' in request.form and 'age' in request.form:
        patient_id = request.form['patient_id']
        patient_name = request.form['patient_name']
        sex = request.form['sex']
        age = request.form['age']
        start_time = request.form['start_time']
        diagnosis_time = request.form['diagnosis_time']
        print(patient_name, sex, age)
        cursor.execute(
            'update patient_info set patient_name=%s ,sex=%s,age=%s,start_time=%s,diagnosis_time=%s where patient_id=%s',
            (patient_name, sex, age, start_time, diagnosis_time, patient_id))
        db.commit()
        mesage2 = '修改成功'
    return render_template('alter_patient.html', data=result, mesage1=mesage1, mesage2=mesage2)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

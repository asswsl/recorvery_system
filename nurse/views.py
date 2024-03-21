from flask import Flask, render_template, request, redirect, url_for, session
from sql import cursor, db
from datetime import date
from nurse import nurse_blue


# 护士站首页
@nurse_blue.route('/nurse')
def nurse():
    cursor.execute('select * from patient_info')
    result = cursor.fetchall()
    return render_template('nurse.html', data=result)


@nurse_blue.route('/treat_info', methods=['POST', 'GET'])
def treat_info():
    cursor.execute('select * from treat_info')
    check_result = cursor.fetchall()
    return render_template('treat_info.html', data=check_result)


# 增加患者信息
@nurse_blue.route('/add_patient', methods=['POST', 'GET'])
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
@nurse_blue.route('/search_patient', methods=['POST', 'GET'])
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
    # print(result)
    return render_template('search_patient.html', data=result, mesage=mesage)


# 删除患者信息
@nurse_blue.route('/delete_patient', methods=['POST', 'GET'])
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
        cursor.execute('select * from patient_info where patient_id=%s', del_id)
        test = cursor.fetchall()
        if not test:
            mesage = '删除成功'
        else:
            mesage = '删除失败'
    return render_template('delete_patient.html', data=result, mesage=mesage)


# 修改患者信息
@nurse_blue.route('/alter_patient', methods=['POST', 'GET'])
def alter_patient():
    mesage1 = ''
    mesage2 = ''
    result = ''
    if request.method == 'POST' and 'patient_id' in request.form:
        patient_id = request.form['patient_id']
        cursor.execute('select * from patient_info where patient_id=%s', (patient_id))
        result = cursor.fetchone()
        # print(result)
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
        # print(patient_name, sex, age)
        cursor.execute(
            'update patient_info set patient_name=%s ,sex=%s,age=%s,start_time=%s,diagnosis_time=%s where patient_id=%s',
            (patient_name, sex, age, start_time, diagnosis_time, patient_id))
        db.commit()
        mesage2 = '修改成功'
    return render_template('alter_patient.html', data=result, mesage1=mesage1, mesage2=mesage2)


# 搜索治疗信息
@nurse_blue.route('/search_treat', methods=['POST', 'GET'])
def search_treat():
    mesage = ''
    result = ''
    fields = ['patient_id', 'patient_name', 'sex', 'age', 'doctor', 'treatments', 'total_numbers', 'used_numbers']
    if request.method == 'POST' and 'data' in request.form and 'kind' in request.form:
        kind = request.form['kind']
        data = request.form['data']
        if kind not in fields:
            mesage = '错误查询'
        elif not data:
            mesage = '请填写查询数据'
        else:
            cursor.execute('select * from treat_info where %s=%%s' % kind, (data,))
            result = cursor.fetchall()
            if not result:
                mesage = '不存在信息'
            else:
                mesage = '查询成功'
            # print(result)
    return render_template('search_treat.html', data=result, mesage=mesage)


# 增加治疗信息
@nurse_blue.route('/add_treat', methods=['POST', 'GET'])
def add_treat():
    mesage = ''
    if request.method == 'POST' and 'patient_name' in request.form and 'age' in request.form and 'patient_id' in request.form:
        patient_name = request.form['patient_name']
        sex = request.form['sex']
        age = request.form['age']
        patient_id = request.form['patient_id']
        doctor = request.form['doctor']
        treatments = request.form['treatments']
        total_numbers = request.form['total_numbers']
        cursor.execute('select * from treat_info where patient_name=%s and sex=%s and age=%s and patient_id=%s',
                       (patient_name, sex, age, patient_id))
        account = cursor.fetchone()
        cursor.execute('select * from treat_info where patient_id=%s', patient_id)
        id = cursor.fetchone()
        if account:
            mesage = '患者已存在 !'
        elif id:
            mesage = '患者卡号不能相同'
        elif not patient_name or not age or not patient_id:
            mesage = '请全部填写!'
        else:
            cursor.execute('insert into treat_info values (%s,%s,%s,%s,%s,%s,%s,%s)',
                           (patient_id, patient_name, sex, age, doctor, treatments, total_numbers, 0))
            db.commit()
            mesage = '增加成功!'
    elif request.method == 'POST':
        mesage = '请全部填写 !'
    return render_template('add_treat.html', mesage=mesage)

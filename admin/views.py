from flask import Flask, render_template, request, redirect, url_for, session
import re
from sql import cursor, db
from datetime import date
from admin import admin_blue


# 管理员界面
@admin_blue.route('/admin')
def admin():
    return render_template('admin.html')


# 设备信息浏览
@admin_blue.route('/device_info', methods=['POST', 'GET'])
def device_info():
    cursor.execute('select * from device_info where end_time is null')
    result = cursor.fetchall()
    return render_template('device_info.html', data=result)


# 设备信息查找
@admin_blue.route('/device_search', methods=['POST', 'GET'])
def device_search():
    mesage = ''
    search_result = ''
    fields = ['device_id', 'device_name', 'device_type', 'device_own', 'start_time', 'end_time']
    if request.method == 'POST' and 'data' in request.form and 'kind' in request.form:
        kind = request.form['kind']
        data = request.form['data']
        if kind not in fields:
            mesage = '错误查询'
        elif not data:
            mesage = '请填写查询数据'
        else:
            cursor.execute('select * from device_info where %s=%%s' % kind, (data,))
            search_result = cursor.fetchall()
            if not search_result:
                mesage = '不存在信息'
            else:
                mesage = '查询成功'
            # print(result)
    # 在查询后，总列表仍能显示
    cursor.execute('select * from device_info where end_time is null')
    result = cursor.fetchall()
    return render_template('device_info.html', data=result, search_data=search_result, mesage=mesage)


# 新增设备信息
@admin_blue.route('/device_add', methods=['POST', 'GET'])
def device_add():
    mesage = ''
    if request.method == 'POST' and 'device_id' in request.form and 'device_name' in request.form and 'device_type' in request.form and 'device_own' in request.form:
        device_id = request.form['device_id']
        device_name = request.form['device_name']
        device_type = request.form['device_type']
        device_own = request.form['device_own']
        start_time = request.form['start_time']
        cursor.execute(
            'select * from device_info where device_id=%s and device_name=%s and device_type=%s and device_own=%s',
            (device_id, device_name, device_type, device_own))
        device = cursor.fetchone()
        cursor.execute('select * from device_info where device_id=%s', device_id)
        id = cursor.fetchone()
        if device:
            mesage = '设备已存在 !'
        elif id:
            mesage = '设备编号不能相同'
        elif not device_id or not device_name or not device_type:
            mesage = '请全部填写!'
        else:
            cursor.execute('insert into device_info values (%s,%s,%s,%s,%s,%s)',
                           (device_id, device_name, device_type, device_own, start_time, None))
            db.commit()
            mesage = '增加成功!'
    elif request.method == 'POST':
        mesage = '请全部填写 !'
    return render_template('device_add.html', mesage=mesage)


# 设备报废 不能用删除的思路，应当添加报废日期
@admin_blue.route('/device_delete', methods=['POST', 'GET'])
def device_delete():
    mesage = ''
    cursor.execute('select * from device_info where end_time is null ')
    result = cursor.fetchall()
    end_time = date.today()
    if request.method == 'POST' and 'id' in request.form:
        device_id = request.form['id']
        cursor.execute('update device_info set end_time = %s where device_id = %s', (end_time, device_id))
        db.commit()
        # 点击后刷新表格
        cursor.execute('select * from device_info where end_time is null ')
        result = cursor.fetchall()
        # resu = cursor.execute('select * from patient_info where patient_id=%s', del_id)
        if not result:
            mesage = '报废成功'
        else:
            mesage = '报废失败'
    return render_template('device_delete.html', data=result, mesage=mesage)


# 管理员页面--医师
@admin_blue.route('/doctor_info', methods=['POST', 'GET'])
def doctor_info():
    cursor.execute('select * from doctor_info')
    result = cursor.fetchall()
    return render_template('doctor_info.html', data=result)


# 查询医师信息
@admin_blue.route('/doctor_search', methods=['POST', 'GET'])
def doctor_search():
    mesage = ''
    search_result = ''
    fields = ['doctor_id', 'doctor_name', 'sex', 'age', 'department', 'title']
    if request.method == 'POST' and 'data' in request.form and 'kind' in request.form:
        kind = request.form['kind']
        data = request.form['data']
        if kind not in fields:
            mesage = '错误查询'
        elif not data:
            mesage = '请填写查询数据'
        else:
            cursor.execute('select * from doctor_info where %s=%%s' % kind, (data,))
            search_result = cursor.fetchall()
            if not search_result:
                mesage = '不存在信息'
            else:
                mesage = '查询成功'
            # print(result)\
    # 在查询后，总列表仍能显示
    cursor.execute('select * from doctor_info')
    result = cursor.fetchall()
    return render_template('doctor_info.html', data=result, search_data=search_result, mesage=mesage)


# 增加医师
@admin_blue.route('/doctor_add', methods=['POST', 'GET'])
def doctor_add():
    mesage = ''
    if request.method == 'POST':
        # 检查是否所有必需的字段都在表单中
        required_fields = ['doctor_id', 'doctor_name', 'sex', 'age', 'department', 'title']
        if all(field in request.form for field in required_fields):
            doctor_id = request.form['doctor_id']
            doctor_name = request.form['doctor_name']
            sex = request.form['sex']
            age = request.form['age']
            department = request.form['department']
            title = request.form['title']
            # 检查医生是否已存在
            cursor.execute(
                'SELECT * FROM doctor_info WHERE doctor_id = %s AND doctor_name = %s AND sex = %s AND age = %s AND '
                'department = %s AND title = %s',
                (doctor_id, doctor_name, sex, age, department, title))
            doctor = cursor.fetchone()
            # 检查医生编号是否已存在
            cursor.execute('SELECT * FROM doctor_info WHERE doctor_id = %s', (doctor_id,))
            id_exists = cursor.fetchone()
            if doctor:
                mesage = '医师已存在！'
            elif id_exists:
                mesage = '医师编号不能相同'
            else:
                # 将新医生插入数据库
                cursor.execute('INSERT INTO doctor_info VALUES (%s, %s, %s, %s, %s, %s)',
                               (doctor_id, doctor_name, sex, age, department, title))
                db.commit()
                mesage = '增加成功'
        else:
            # 如果没有提供所有字段
            mesage = '请全部填写'
    return render_template('doctor_add.html', mesage=mesage)


# 删除医师信息
@admin_blue.route('/doctor_delete', methods=['POST', 'GET'])
def doctor_delete():
    mesage = ''
    cursor.execute('select * from doctor_info')
    result = cursor.fetchall()
    if request.method == 'POST' and 'doctor_id' in request.form:
        doctor_id = request.form['doctor_id']
        cursor.execute('delete from doctor_info where doctor_id = %s ', doctor_id)
        db.commit()
        # 刷新
        cursor.execute('select * from doctor_info')
        result = cursor.fetchall()
        cursor.execute('select * from doctor_info where doctor_id=%s', doctor_id)
        test = cursor.fetchall()
        if not test:
            mesage = '删除成功'
        else:
            mesage = '删除失败'
    return render_template('doctor_delete.html', data=result, mesage=mesage)


# 修改医师信息
@admin_blue.route('/doctor_alter', methods=['POST', 'GET'])
def doctor_alter():
    mesage1 = ''
    mesage2 = ''
    result = ''
    if request.method == 'POST' and 'doctor_id' in request.form:
        doctor_id = request.form['doctor_id']
        cursor.execute('select * from doctor_info where doctor_id=%s', (doctor_id))
        result = cursor.fetchone()

        if not result:
            mesage1 = '查询失败'
        else:
            mesage1 = '查询成功'

    if request.method == 'POST' and 'doctor_name' in request.form and 'sex' in request.form and 'age' in request.form:
        doctor_id = request.form['doctor_id']
        doctor_name = request.form['doctor_name']
        sex = request.form['sex']
        age = request.form['age']
        department = request.form['department']
        title = request.form['title']

        cursor.execute(
            'update doctor_info set doctor_name=%s , sex=%s, age=%s, department=%s , title=%s where doctor_id=%s',
            (doctor_name, sex, age, department, title, doctor_id))
        db.commit()
        mesage2 = '修改成功'
    return render_template('doctor_alter.html', data=result, mesage1=mesage1, mesage2=mesage2)


# 管理员页面--治疗项目
@admin_blue.route('/treatment_info', methods=['POST', 'GET'])
def treatment_info():
    cursor.execute('select * from treatment_info')
    result = cursor.fetchall()
    return render_template('treatment_info.html', data=result)


# 查询治疗项目信息
@admin_blue.route('/treatment_search', methods=['POST', 'GET'])
def treatment_search():
    mesage = ''
    search_result = ''
    fields = ['treat_id', 'treat_name', 'treat_type', 'treat_numbers']
    if request.method == 'POST' and 'data' in request.form and 'kind' in request.form:
        kind = request.form['kind']
        data = request.form['data']
        if kind not in fields:
            mesage = '错误查询'
        elif not data:
            mesage = '请填写查询数据'
        else:
            cursor.execute('select * from treatment_info where %s=%%s' % kind, (data,))
            search_result = cursor.fetchall()
            if not search_result:
                mesage = '不存在信息'
            else:
                mesage = '查询成功'
            # print(result)\
    # 在查询后，总列表仍能显示
    cursor.execute('select * from treatment_info')
    result = cursor.fetchall()
    return render_template('treatment_info.html', data=result, search_data=search_result, mesage=mesage)


# 增加治疗项目
@admin_blue.route('/treatment_add', methods=['POST', 'GET'])
def treatment_add():
    mesage = ''
    if request.method == 'POST':
        # 检查是否所有必需的字段都在表单中
        required_fields = ['treat_id', 'treat_name', 'treat_type', 'treat_numbers']
        if all(field in request.form for field in required_fields):
            treat_id = request.form['treat_id']
            treat_name = request.form['treat_name']
            treat_type = request.form['treat_type']
            treat_numbers = request.form['treat_numbers']
            # 检查项目是否已存在
            cursor.execute(
                'SELECT * FROM treatment_info WHERE treat_id = %s AND treat_name = %s AND treat_type = %s AND treat_numbers = %s',
                (treat_id, treat_name, treat_type, treat_numbers))
            treatment = cursor.fetchone()
            # 检查医生编号是否已存在
            cursor.execute('SELECT * FROM treatment_info WHERE treat_id = %s', (treat_id,))
            id_exists = cursor.fetchone()
            if treatment:
                mesage = '治疗项目已存在！'
            elif id_exists:
                mesage = '项目编号不能相同'
            else:
                # 将新医生插入数据库
                cursor.execute('INSERT INTO treatment_info VALUES (%s, %s, %s, %s)',
                               (treat_id, treat_name, treat_type, treat_numbers))
                db.commit()
                mesage = '增加成功'
        else:
            # 如果没有提供所有字段
            mesage = '请全部填写'
    return render_template('treatment_add.html', mesage=mesage)


@admin_blue.route('/treatment_delete', methods=['POST', 'GET'])
def treatment_delete():
    mesage = ''
    cursor.execute('select * from treatment_info')
    result = cursor.fetchall()
    if request.method == 'POST' and 'treat_id' in request.form:
        treat_id = request.form['treat_id']
        cursor.execute('delete from treatment_info where treat_id = %s ', treat_id)
        db.commit()
        # 刷新
        cursor.execute('select * from treatment_info')
        result = cursor.fetchall()
        cursor.execute('select * from treatment_info where treat_id=%s', treat_id)
        test = cursor.fetchall()
        if not test:
            mesage = '删除成功'
        else:
            mesage = '删除失败'
    return render_template('treatment_delete.html', data=result, mesage=mesage)


# 修改治疗项目信息
@admin_blue.route('/treatment_alter', methods=['POST', 'GET'])
def treatment_alter():
    mesage1 = ''
    mesage2 = ''
    result = ''
    if request.method == 'POST' and 'treat_id' in request.form:
        treat_id = request.form['treat_id']
        cursor.execute('select * from treatment_info where treat_id=%s', (treat_id))
        result = cursor.fetchone()

        if not result:
            mesage1 = '查询失败'
        else:
            mesage1 = '查询成功'

    if request.method == 'POST' and 'treat_id' in request.form and 'treat_name' in request.form and 'treat_type' in request.form and 'treat_numbers' in request.form:
        treat_id = request.form['treat_id']
        treat_name = request.form['treat_name']
        treat_type = request.form['treat_type']
        treat_numbers = request.form['treat_numbers']
        cursor.execute(
            'update treatment_info set treat_name=%s , treat_type=%s, treat_numbers=%s where treat_id=%s',
            (treat_name, treat_type, treat_numbers, treat_id))
        db.commit()
        mesage2 = '修改成功'
    return render_template('treatment_alter.html', data=result, mesage1=mesage1, mesage2=mesage2)

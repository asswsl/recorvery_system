from flask import Flask, render_template, request, redirect, url_for, session
import re
from sql import cursor, db
from datetime import date
from doctor import doctor_blue


# 医生端主页面
@doctor_blue.route('/doctor')
def doctor():
    return render_template('doctor.html')


# 浏览患者简略信息
@doctor_blue.route('/doctor_patientInfo')
def doctor_patientInfo():
    cursor.execute('select * from treat_info')
    result = cursor.fetchall()
    return render_template('doctor_patientInfo.html', data=result)


# 搜索患者信息
@doctor_blue.route('/doctor_searchPatient', methods=['POST', 'GET'])
def doctor_searchPatient():
    mesage = ''
    result = ''
    fields = ['patient_id', 'patient_name', 'sex', 'age']
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
    return render_template('doctor_searchPatient.html', mesage=mesage, data=result)


# 患者详细信息界面
@doctor_blue.route('/doctor_detailsInfo', methods=['POST', 'GET'])
def doctor_detailsInfo():

    id = request.form['patient_id']
    cursor.execute('select * from treat_info where patient_id=%s', (id))
    result = cursor.fetchone()
    cursor.execute('select * from prescription_info where patient_id=%s', (id))
    medicine = cursor.fetchall()
    print(result)
    return render_template('doctor_detailsInfo.html', data=result, medicine=medicine)


# 为患者开方
@doctor_blue.route('/doctor_medicine', methods=['POST', 'GET'])
def doctor_medicine():
    id = request.form['patient_id']
    medicine_name = request.form['medicine_name']
    medicine_number = request.form['medicine_number']
    cursor.execute('select * from treat_info where patient_id=%s', (id))
    patient = cursor.fetchone()
    # print(patient, medicine_name,medicine_number)
    cursor.execute('insert into prescription_info values (%s,%s,%s,%s,%s,%s)',
                   (patient[0], patient[1], patient[2], patient[3], medicine_name, medicine_number))
    db.commit()
    return render_template('doctor_detailsInfo.html', data=patient)


# 修改患者信息
@doctor_blue.route('/doctor_alterPatient', methods=['POST', 'GET'])
def doctor_alterPatient():
    mesage1 = ''
    mesage2 = ''
    result1 = ''
    result2 = ''
    if request.method == 'POST' and 'patient_id' in request.form:
        patient_id = request.form.get('patient_id')
        cursor.execute('select * from treat_info where patient_id=%s', (patient_id))
        result1 = cursor.fetchone()
        cursor.execute('select * from prescription_info where patient_id=%s', (patient_id))
        result2 = cursor.fetchone()
        print(result2)
        if not result1 and not result2:
            mesage1 = '查询失败'
        else:
            mesage1 = '查询成功'
    if request.method == 'POST' and 'patient_name' in request.form and 'sex' in request.form and 'age' in request.form:
        patient_id = request.form.get('id')
        patient_name = request.form.get('patient_name')
        sex = request.form.get('sex')
        age = request.form.get('age')
        doctor = request.form.get('doctor')
        depart = request.form.get('depart')
        treatments = request.form.get('treatments')
        medicine_name = request.form.get('medicine_name')
        medicine_number = request.form.get('medicine_number')
        print(patient_id, patient_name, sex, age, doctor, depart, treatments, medicine_name, medicine_number)
        cursor.execute(
            'update treat_info set patient_name=%s , sex=%s, age=%s, doctor=%s,depart=%s ,treatments=%s where patient_id=%s',
            (patient_name, sex, age, doctor, depart, treatments, int(patient_id)))
        db.commit()
        cursor.execute('update prescription_info set medicine_name=%s,medicine_number=%s where patient_id=%s',
                       (medicine_name, medicine_number,int(patient_id)))
        db.commit()
        mesage2 = '修改成功'
    return render_template('doctor_alterPatient.html', data1=result1, data2=result2, mesage1=mesage1, mesage2=mesage2)


# 动态表格分析患者数据
@doctor_blue.route('/doctor_chart')
def doctor_chart():
    # 获取病症名称以及数量
    cursor.execute('select treatments, COUNT(1) AS counts FROM treat_info GROUP BY treatments')
    treatments_counts = cursor.fetchall()
    # 获取就诊部门名称以及数量
    cursor.execute('select depart, COUNT(1) AS counts FROM treat_info GROUP BY depart')
    depart_counts = cursor.fetchall()
    for item in depart_counts:
        print(item[0], item[1])

    return render_template('doctor_chart.html', data1=treatments_counts, data2=depart_counts)

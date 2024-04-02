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
    return render_template('doctor_searchPatient.html',mesage=mesage,data=result)


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

import datetime

from flask import Flask, render_template, request, redirect, url_for, session
import re
from sql import cursor, db
from datetime import date
from treat import treat_blue


# 治疗端界面

@treat_blue.route('/treat')
def treatstation():
    return render_template('treatstation.html')


# 护士排班设置
@treat_blue.route('/treatstation_dates', methods=['POST', 'GET'])
def treatstation_dates():
    cursor.execute('select name from user where rol="护士站"')
    result = cursor.fetchall()
    # nurse_1: 0-6 nurse_2: 6-12 nurse_3: 12-18 nurse_4: 18-0
    date = request.form.get('duty_time')
    if date=='':
        msg='日期未填写'
        print(msg)
    else:
        nurse1 = request.form.get('nurse_1',None)
        nurse2 = request.form.get('nurse_2',None)
        nurse3 = request.form.get('nurse_3',None)
        nurse4 = request.form.get('nurse_4',None)
        nursing_times = [('0-6', nurse1), ('6-12', nurse2), ('12-18', nurse3), ('18-0', nurse4)]
        for time, nurse in nursing_times:
            time = str(date) + ' ' + str(time)
            cursor.execute("INSERT INTO treatstation (nurse_name, duty_time)VALUES (%s, %s)", (nurse, time))
            db.commit()
    return render_template('treatstation_dates.html', data=result)

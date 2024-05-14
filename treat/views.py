import datetime

from flask import Flask, render_template, request, redirect, url_for, session
import re
from sql import cursor, db
from datetime import date
from treat import treat_blue

#治疗端界面

@treat_blue.route('/treat')
def treatstation():
    return render_template('treatstation.html')


#护士排班设置
@treat_blue.route('/treatstation_dates',methods=['POST','GET'])
def treatstation_dates():
    cursor.execute('select name from user where rol="护士站"')
    result=cursor.fetchall()
    fileds=['nurse1','nurse2','nurse3','nurse4','duty_time']
    # if all(field in request.form for  field in fileds):
    #nurse_1: 0-6 nurse_2: 6-12 nurse_3: 12-18 nurse_4: 18-0
    nurse1 = request.form['nurse_1']
    nurse2 = request.form['nurse_2']
    nurse3 = request.form['nurse_3']
    nurse4 = request.form['nurse_4']
    date   = request.form['duty_time']
    print(nurse1,nurse2,nurse3,nurse4,date)
    # date1   = datetime.datetime.strptime(date, "%Y-%m-%d")
    # print(date1)
    # date2   = datetime.datetime(date1.year, date1.month, date1.day)
    # print(date2)
    nursing_times = [('0-6', nurse1), ('6-12', nurse2), ('12-18', nurse3), ('18-0', nurse4)]
    for time, nurse in nursing_times:
        time=date+' '+time
        print(time)
        cursor.execute("INSERT INTO treatstation (nurse_name, duty_time)VALUES (?, ?)", (nurse, time))

    return render_template('treatstation_dates.html',data=result)



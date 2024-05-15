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

@treat_blue.route('/treatstation_patientInfo', methods=['POST', 'GET'])
def treatstation_patientInfo():
    cursor.execute('select * from treat_info')
    result = cursor.fetchall()
    return render_template('doctor_patientInfo.html', data=result)

@treat_blue.route('/treatstation_duty', methods=['POST', 'GET'])
def treatstation_duty():
    cursor.execute('''
            SELECT 
                nurse_name, 
                duty_time AS Date, 
                SUBSTRING_INDEX(duty_time, ' ', -1) AS TimePeriod,
                DAYNAME(STR_TO_DATE(duty_time, '%Y-%m-%d')) AS Weekday, 
                STR_TO_DATE(SUBSTRING_INDEX(duty_time, ' ', 1), '%Y-%m-%d') AS DateOnly,
                patient, 
                doctor_name, 
                patient_nurse, 
                patient_doctor, 
                treatment_plan 
            FROM 
                treatstation 
            ORDER BY 
                STR_TO_DATE(duty_time, '%Y-%m-%d'), nurse_name;
        ''')

    weekdays = []
    hours = []
    nurse = []
    day = []
    results = cursor.fetchall()
    for row in results:
        nurse.append(row[0])
        hours.append(row[2])
        weekdays.append(row[3])
        day.append(row[4])

    nurse_schedule = []

    schedule = {
        'nurse_name': nurse,
        'weekday': weekdays,
        'day': day,
        'hours': hours,
    }
    nurse_schedule.append(schedule)
    now = datetime.datetime.now().date()
    print(now)
    # 提取出前端选择的日期
    selected_date = request.form.get('date')
    if selected_date == None:
        selected_date = str(now)
    print(selected_date)

    #计算日期所在周
    week = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
    start_week = week - datetime.timedelta(days=week.weekday())
    end_week = start_week + datetime.timedelta(days=7)

    # 先生成一个空的字典

    nurse_table = {}

    # 注意我们在这里获取字典的时候增加了[0]
    for i in range(len(nurse_schedule[0]["nurse_name"])):
        nurse = nurse_schedule[0]["nurse_name"][i]
        weekday = nurse_schedule[0]["weekday"][i]
        # day = nurse_schedule[0]["day"][i]
        hours = nurse_schedule[0]["hours"][i]

        try:
            day = datetime.datetime.strptime(str(nurse_schedule[0]["day"][i]), '%Y-%m-%d')
        except ValueError:
            continue

        # 如果selected_day在那周的日期范围内并且其它所有条件满足我们才进行处理
        if start_week <= day <= end_week and all((nurse, weekday, hours)) and hours in ["0-6", "6-12", "12-18",
                                                                                            "18-0"]:
            key = f"{day.strftime('%Y-%m-%d')}-{weekday}-{hours}"
            if key not in nurse_table:
                nurse_table[key] = []
            nurse_table[key].append(nurse)

        # # 如果selected_date等于day，并且剩余所有条件全部满足，我们才处理这个护士的安排
        # if selected_date == str(day) and all((nurse, weekday, hours)) and hours in ["0-6", "6-12", "12-18", "18-0"]:
        #     key = f"{day}-{weekday}-{hours}"
        #     if key not in nurse_table:
        #         nurse_table[key] = []
        #     nurse_table[key].append(nurse)

    print(nurse_table)

    return render_template('treatstation_duty.html', data=nurse_table)

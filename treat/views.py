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
    print(result)
    return render_template('treatstation_dates.html',data=result)
    # return render_template('treatstation_dates.html')
    # date_str = request.form.get('nurse1')

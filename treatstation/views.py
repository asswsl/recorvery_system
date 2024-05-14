from flask import Flask, render_template, request, redirect, url_for, session
import re
from sql import cursor, db
from datetime import date
from treatstation import treatstation_blue

#治疗端界面

@treatstation_blue.route('/treatstation')
def treatstation():
    return render_template('treatstation.html')


#护士排班设置
@treatstation_blue.route('/treatstation_dates', methods=['POST', 'GET'])
def treatstation_dates():
    cursor.execute("SELECT name FROM user WHERE rol = '护士站'")
    result = cursor.fetchall()
    print(result)
    return render_template('treatstation_dates.html', data=result)

    # date_str = request.form.get('nurse1')

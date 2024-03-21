import pymysql

db = pymysql.connect(host="localhost", user="root", password="ys124126", database="recorvery_system",
                     charset="utf8")
cursor = db.cursor()

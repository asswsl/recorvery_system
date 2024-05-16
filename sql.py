import pymysql

db = pymysql.connect(host="localhost", user="root", password="mgm81849117415", database="recorvery_system",
                     charset="utf8")
cursor = db.cursor()

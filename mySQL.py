import pymysql
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# Open database connection
host = ""
port = 3306
username =""
password = ""
database = ""

fieldnames=[]
with open('config.json') as json_data:
    config = json.load(json_data)
    host = config["mysql"]["host"]
    port = config["mysql"]["port"]
    database = config["mysql"]["database"]
    username = config["mysql"]["username"]
    password = config["mysql"]["password"]

def dbConnect():
        global connection
        global db
        connection = pymysql.connect(host=host,
                                     user=username,
                                     password=password,
                                     db=database,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        db = connection.db





def getAllfield(table):
    result = []
    if connection.open == 0 :
        dbConnect()
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s'"
            cursor.execute(sql, database, table)
            results = cursor.fetchall()
            for row in results:
                result.append(row[0])
            print(result)
    except:
        print "Error: unable to fecth data"
    finally:
        return result

#add
def insert(table,values):
    success = True
    if connection.open == 0 :
        dbConnect()
    fieldnames = getAllfield(table)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "INSERT INTO %s (%s) VALUES ('%s')"
            cursor.execute(sql, table, ','.join(fieldnames), "','".join(''.join(elems) for elems in values))
            connection.commit()
    except db.Error, e:
        print "Error: unable to insert data. {%s}" % str(e)
        # Rollback in case there is any error
        db.rollback()
        success = False
    finally:
        return success


def insertAutoInId(table,values):
    success = True
    if connection.open == 0:
        dbConnect()
    fieldnames = getAllfield(table)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "INSERT INTO %s (%s) VALUES ('%s')"
            cursor.execute(sql, table, ','.join(fieldnames), "','".join(''.join(elems) for elems in values))
            connection.commit()
    except db.Error, e:
        print "Error: unable to insert data. {%s}" % str(e)
        # Rollback in case there is any error
        db.rollback()
        success = False
    finally:
        return success

#update
def update(table,values,condition):
    success = True
    if connection.open == 0:
        dbConnect()
    fieldnames = getAllfield(table)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            update = []
            for i in range(0, len(fieldnames)):
                update.append(fieldnames[i] + "= \"%s\"" % values[i])
            sql = "UPDATE %s SET %s WHERE %s"
            cursor.execute(sql, table,', '.join(str(x) for x in update) ,condition)
            result = cursor.fetchone()
    except db.Error, e:
        print "Error: unable to insert data. {%s}" % str(e)
        # Rollback in case there is any error
        db.rollback()
        success = False
    finally:
        return success

def dbClose():
	# disconnect from server
	cursor=0
	db.close()

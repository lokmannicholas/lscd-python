import MySQLdb
import sys
import json
reload(sys)
sys.setdefaultencoding("utf-8")
# Open database connection
host = ""
port = 3306
username =""
password = ""
database = ""
cursor = 0
fieldnames=[]

with open('config.json') as json_data:
    config = json.load(json_data)
    host = config["mysql"]["host"]
    port = config["mysql"]["port"]
    database = config["mysql"]["database"]
    username = config["mysql"]["username"]
    password = config["mysql"]["password"]

def dbConnect():
    global db
    global cursor

    db = MySQLdb.connect(host=host,port=port,user=username,passwd=password)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    sql = "CREATE DATABASE IF NOT EXISTS %s CHARACTER SET utf8 COLLATE utf8_general_ci " % database
    cursor.execute(sql)
    db = MySQLdb.connect(host=host, port=port, user=username, passwd=password,db=database,use_unicode=True, charset="utf8")
    cursor = db.cursor()


def setTable(table):
    if cursor == 0:
        dbConnect()
    sql = "CREATE TABLE IF NOT EXISTS `%s`( `id` int(11) NOT NULL, `class` varchar(45) DEFAULT NULL, `name` varchar(45) DEFAULT NULL, `startdate` date DEFAULT NULL, `enddate` date DEFAULT NULL, `starttime` time DEFAULT NULL, `endtime` time DEFAULT NULL, `weekday` varchar(45) DEFAULT NULL, `location` varchar(45) DEFAULT NULL, `age` varchar(45) DEFAULT NULL, `fee` int(11) DEFAULT NULL, `quota` int(11) DEFAULT NULL, `quota_remain` int(11) DEFAULT NULL, `enrolment_startdate` date DEFAULT NULL, `enrolment_enddate` date DEFAULT NULL, `balloting` date DEFAULT NULL, `enrolment_remain_startdate` date DEFAULT NULL, `enrolment_remain_enddate` date DEFAULT NULL, `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table
    cursor.execute(sql)



def getAllfield(table):
    if cursor==0:
        dbConnect()
    sql="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='%s' AND TABLE_NAME='%s'" % (database,table)
    result=[]
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            result.append(row[0])
    except:
        print "Error: unable to fecth data"
    return result


#add
def insert(table,values):
    if cursor==0:
        dbConnect()
	fieldnames=getAllfield(table)
	sql="INSERT INTO %s (%s) VALUES ('%s')" % (table,','.join(fieldnames),"','".join(''.join(elems) for elems in values))
	print "sql: {%s}" % str(sql)
	success=True
	try:
		cursor.execute(sql)
		db.commit()
	except MySQLdb.Error,e:
		print "Error: unable to insert data. {%s}" % str(e)
   		# Rollback in case there is any error
   		db.rollback()
		success=False
	data = cursor.fetchone()
	dbClose()
	return success

def insertAutoInId(table,values):
    if cursor == 0:
        dbConnect()
    fieldnames=getAllfield(table)
    fieldnames.remove('id')
    sql="INSERT INTO %s (%s) VALUES ('%s')" % (table,','.join(fieldnames),"','".join(''.join(elems) for elems in values))
    success=True
    try:
        cursor.execute(sql)
        db.commit()
    except MySQLdb.Error,e:
        print "Error: unable to insert data. {%s}" % str(e)
        # Rollback in case there is any error
        db.rollback()
        success=False
    data = cursor.fetchone()
    dbClose()
    return success


#update
def update(table,values,condition):
    if cursor == 0:
        dbConnect()
    fieldnames = getAllfield(table)
    update = []
    for i in range(0, len(fieldnames)):
        update.append(fieldnames[i] + "= \"%s\"" % values[i])
        sql = "UPDATE %s SET %s WHERE %s" % (table, ', '.join(str(x) for x in update), condition)
        print "sql: {%s}" % str(sql)
    success = True
    try:
        cursor.execute(sql)
        db.commit()
    except MySQLdb.Error, e:
        print "Error: unable to update data.{%s}" % str(e)
    # Rollback in case there is any error
        db.rollback()
        success = False
        data = cursor.fetchone()
        dbClose()
    return success

#ids
def getId(table):
    if cursor == 0:
        dbConnect()
    sql="SELECT id FROM %s" % (table)
    result=[]
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            result.append(row[0])
    except:
        print "Error: unable to fecth data"
    dbClose()
    return result


def getUpdateId(table):
    if cursor == 0:
        dbConnect()
    sql = "SELECT id FROM %s where startdate > current_date() AND balloting <= current_date() ORDER BY id DESC;" % table
    result = []
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            result.append(row[0])
    except:
        print "Error: unable to fecth data"

    dbClose()
    return result

#execute
def execute(cmd):
    if cursor == 0:
        dbConnect()
    sql = "%s" % cmd
    success = True
    try:
        cursor.execute("USE %s;" % database);
        cursor.execute(sql)
        db.commit()

    except MySQLdb.Error, e:
        print "Error: execute failed. {%s}" % str(e)
        # Rollback in case there is any error
        db.rollback()
        success = False
    cursor.fetchone()
    dbClose()
    return success

#get column
def getColumn(table,column):
    if cursor == 0:
        dbConnect()
    sql="SELECT %s FROM %s" %  (column,table)
    result=[]
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            result.append(row)
    except:
        print "Error: unable to fecth data"
    dbClose()
    return result


#fetch data
def fetch_data(sql_cmd):
    if cursor == 0:
        dbConnect()
    sql="%s" %  (sql_cmd)
    result=[]
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            result.append(row[0])
    except:
        print "Error: unable to fecth data"
	dbClose()
	return result

def dbClose():
	# disconnect from server
	cursor=0
	db.close()

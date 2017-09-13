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
def dbInit():
    global db
    global cursor

    db = MySQLdb.connect(host=host,port=port,user=username,passwd=password)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    sql = "CREATE DATABASE IF NOT EXISTS %s CHARACTER SET utf8 COLLATE utf8_general_ci " % database
    cursor.execute(sql)
    dbConnect()

def dbConnect():
    global db
    global cursor
    db = MySQLdb.connect(host=host, port=port, user=username, passwd=password,db=database,use_unicode=True, charset="utf8")
    cursor = db.cursor()


def setTable(table):
    dbConnect()
    sql = "CREATE TABLE IF NOT EXISTS `%s`( `id` int(11) NOT NULL, `class` varchar(45) DEFAULT NULL, `name` varchar(45) DEFAULT NULL, `startdate` date DEFAULT NULL, `enddate` date DEFAULT NULL, `starttime` time DEFAULT NULL, `endtime` time DEFAULT NULL, `weekday` varchar(45) DEFAULT NULL, `location` varchar(45) DEFAULT NULL, `age` varchar(45) DEFAULT NULL, `fee` varchar(32) DEFAULT NULL, `quota` varchar(32) DEFAULT NULL, `quota_remain` varchar(32) DEFAULT NULL, `enrolment_startdate` date DEFAULT NULL, `enrolment_enddate` date DEFAULT NULL, `balloting` date DEFAULT NULL, `enrolment_remain_startdate` date DEFAULT NULL, `enrolment_remain_enddate` date DEFAULT NULL, `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table
    try:
        cursor.execute(sql)
    except MySQLdb.Error,e:
        print "Error: unable to upsert data. {%s}" % str(e)
        db.rollback()
    finally:
        dbClose()


#add
def upsert(table,dic):
    dbConnect()
    fieldnames=[]
    values=[]
    update = []
    for key in dic:
        fieldnames.append(key)
        values.append(dic[key])
        update.append(" %s = \"%s\"" % (key, dic[key]))

    sql="INSERT INTO %s (%s) VALUES ('%s') on duplicate key update %s ;" % (table,','.join(fieldnames),"','".join(values) , ', '.join(update))
    print "sql: {%s}" % str(sql)
    success=True
    try:
        cursor.execute(sql)
        db.commit()
    except MySQLdb.Error,e:
        print "Error: unable to upsert data. {%s}" % str(e)
        # Rollback in case there is any error
        db.rollback()
        success=False
    finally:
        dbClose()
    return success

def dbClose():
	db.close()

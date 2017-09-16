import json
import os.path
import re
import urllib.request
from datetime import datetime

from dateutil.relativedelta import relativedelta

from python36 import Mongo
from python36 import mySQL

# config
storage_file = False
storage_mysql = False
storage_mongo = False
storage_dir = os.path.dirname(os.path.realpath(__file__))+"/data/"

with open('config.json') as json_data:
	config = json.load(json_data)
	storage_file = config["storage"]["file"]
	storage_mysql = config["storage"]["mysql"]
	storage_mongo = config["storage"]["mongo"]
	if config["storage_file"]["path"] != "" :
		storage_dir = config["storage_file"]["path"]
# mysql
if storage_mysql:
	mySQL.dbInit()

#months
date_after_month = datetime.today()+ relativedelta(months=1)
now = datetime.today()
delta_month=[]
for _month in range(0,3):
	delta_month.append(datetime.today()+ relativedelta(months=_month))

#fetch data
#read activites
with open('menu.json' , mode='r', encoding='utf-8') as json_data:
	menu = json.load(json_data)
	for activitie in menu:
		act_table = activitie["act_table"]
		act_code = activitie["act_code"]
		#json file
		storage_file_json=[]
		print ("activity :" + act_table)
		# mysql
		if storage_mysql:
			mySQL.setTable(act_table)
		# for m in range(startMonth,endMonth):
		for m in range(0,len(delta_month)):
			month = int(delta_month[m].month)
			year = int(delta_month[m].year)
			page =1
			print (str(month) + '/' + str(year))
			#check the total class of xxx
			link = "http://www2.lcsd.gov.hk/cf/search/leisure_ora/new_list-ajax.cfm?lang=b5&tarmth=%d&dist=all&en_method=all&en_status=all&age=all&sort_field=pgm_code&sort_order=desc&act=%s&pageno=1&target_type=all&keyword=" % (month ,act_code)

			x = urllib.request.urlopen(link)
			f = x.read()
			myfile = f.decode("utf-8")

			thepage = myfile.find('row-result')
			temp =  myfile[thepage:]
			temp = temp[:temp.find('</p>')]
			m = re.findall(r'\d+', temp)
			temp = m[0]
			if int(temp) < 20 :
				page = 2
			else:
				page  = int(int(temp)/20) + 1

			for i in range(1,page):
				#the link is default as all district, all moths ,all age,all status,,only xxx

				link = "http://www2.lcsd.gov.hk/cf/search/leisure_ora/new_list-ajax.cfm?lang=b5&tarmth=%d&dist=all&en_method=all&en_status=all&age=all&sort_field=pgm_code&sort_order=desc&act=%s&pageno=%d&target_type=all&keyword=" % (month,act_code,i)
				f = urllib.request.urlopen(link)
				f = f.read()
				myfile = f.decode("utf-8")

				start = myfile.find('</thead>')
				end =myfile.find('</table>')
				content = myfile[start:end]

		# 		rows fetch
				list_tr = re.findall(r'(<tr>)',content)
				for tr_index in range(0,len(list_tr)):
					start = content.find('<tr>')
					end =content.find('</tr>')
					row = content[start+4:end]

					#clear HTML tag
		# 			row=row.replace('<br>',' ')
		# 			row=re.sub("<.*?>",'', row)
					regHeader=re.findall(r'(\t|\r|\n)',row)
					for reg in regHeader:
						row=row.replace(reg,'');
					#read rows
		# 			print row

					# HTMLtag = re.compile('[.*?]')
					data=[]
					list_td = re.findall(r'(<td)',row)
					column_count=0
					td = row
					for td_index in range(0,len(list_td)):
						td_start = td.find('<td')
						td_end =td.find('</td>')
						column = td[td_start:td_end]
						column=column.replace('<br>',' ')
						column=re.sub("<.*?>",'', column)

		# 				print column
						# columns in database
						#[ id,class,name,startdate,enddate,starttime,endtime,weekday,location,age,fee,quota,quota_remain,
						#enrolment_startdate,enrolment_enddate,balloting,enrolment_remain_startdate,enrolment_remain_enddate,created_at]
		# 				print column.split()
						if column_count == 0:
							temp = column.split(' ',1)
							data.append(temp[0].strip()) #id
							data.append(temp[1].strip())if len(temp) > 1 else  data.append('') #class

						elif column_count == 1:
							data.append(column) #name
						elif column_count == 2:
							 temp = column.strip().split(' ',2)

							 activity_date = temp[0].split('-',2)

							 activity_date[0] = datetime.strptime(activity_date[0].strip()+'/'+str(year), '%d/%m/%Y').strftime('%Y-%m-%d')
							 data.append(activity_date[0]) #startdate

							 data.append(datetime.strptime(activity_date[1].strip()+'/'+str(year), '%d/%m/%Y').strftime('%Y-%m-%d'))if len(activity_date) > 1 else data.append(activity_date[0]) #enddate

							 activity_time = temp[1].split('-',2)
							 data.append(activity_time[0].strip()+":00") #starttime
							 data.append(activity_time[1].strip()+":00")if len(activity_time) > 1 else data.append(activity_time[0].strip()+":00") #endtime

							 data.append(temp[2]) #weekday

						elif column_count == 3:
							data.append(column.strip()) #location
						elif column_count == 4:
							data.append(column.strip()) #age
						elif column_count == 5:
							data.append(column.strip()) #fee
						elif column_count == 6: #5  (5)
							temp = column.strip().split(' ',1)
							data.append(temp[0].strip()) #quota
							data.append(temp[1].strip()[1:-1])if len(temp) > 1 else  data.append('0') #quota_remain

						elif column_count == 7: #15/09 - 24/09 (30/09) {21/10 - 28/11}
							column = column.replace("@", "")
							temp = column.strip().split()

							#['15/09', '-', '24/09', '(30/09)', '{21/10', '-', '28/11}']
							#enrolment_startdate,enrolment_enddate,balloting,enrolment_remain_startdate,enrolment_remain_enddate,created_at]
							enrolment_startdate = temp[0].strip()
							if len(temp) == 1 :
								data.append(enrolment_startdate)
								data.append('')
							else :
								enrolment_startdate = temp[0].strip()+'/'+str(year) if int(enrolment_startdate[-2:])+2>=month else enrolment_startdate+'/'+str(year+1)
								data.append(datetime.strptime(enrolment_startdate, '%d/%m/%Y').strftime('%Y-%m-%d')) #enrolment_startdate

								enrolment_enddate = temp[2].strip()	+'/'+str(year) if int(temp[2].strip()	[-2:])+2>=month else temp[2].strip()+'/'+str(year+1)
								data.append(datetime.strptime(enrolment_enddate, '%d/%m/%Y').strftime('%Y-%m-%d') )if len(temp) > 2 else data.append(enrolment_startdate) #enrolment_enddate

							if len(temp) > 3 :
								balloting = temp[3].strip()[1:-1]+'/'+str(year) if int(temp[3].strip()[1:-1][-2:])+2>=month else temp[3].strip()[1:-1]+'/'+str(year+1)
								data.append(datetime.strptime(balloting, '%d/%m/%Y').strftime('%Y-%m-%d') )if len(temp) > 3 else data.append(enrolment_startdate) #balloting

								enrolment_remain_startdate = temp[4].strip()[1:]+'/'+str(year) if int(temp[4].strip()[1:][-2:])+2>=month else temp[4].strip()[1:]+'/'+str(year+1)
								data.append( datetime.strptime(enrolment_remain_startdate, '%d/%m/%Y').strftime('%Y-%m-%d'))if len(temp) > 4 else data.append(enrolment_startdate) #enrolment_remain_startdate

								enrolment_remain_enddate =  temp[6].strip()[:-1]+'/'+str(year) if int( temp[6].strip()[:-1][-2:])+2>=month else  temp[6].strip()[:-1]+'/'+str(year+1)
								data.append( datetime.strptime(enrolment_remain_enddate, '%d/%m/%Y').strftime('%Y-%m-%d'))if len(temp) > 6 else data.append(enrolment_startdate) #enrolment_remain_enddate
							else:
								data.append('')
								data.append('')
								data.append('')
						else:
							data.append(str(now))
						td = td[td_end+5:]
						column_count+=1

					#save a record
					activity_json = {}
					if len(data) == 18 :

						if data[0] != "" :
							activity_json["id"] = data[0]
						if data[1] != "" :
							activity_json["class"] = data[1]
						if data[2] != "" :
							activity_json["name"] = data[2]
						if data[3] != "" :
							activity_json["startdate"] = data[3]
						if data[4] != "" :
							activity_json["enddate"] = data[4]
						if data[5] != "" :
							activity_json["starttime"] = data[5]
						if data[6] != "" :
							activity_json["endtime"] = data[6]
						if data[7] != "" :
							activity_json["weekday"] = data[7]
						if data[8] != "" :
							activity_json["location"] = data[8]
						if data[9] != "" :
							activity_json["age"] = data[9]
						if data[10] != "" :
							activity_json["fee"] = data[10]
						if data[11] != "" :
							activity_json["quota"] = data[11]
						if data[12] != "" :
							activity_json["quota_remain"] = data[12]
						if data[13] != "" :
							activity_json["enrolment_startdate"] = data[13]
						if data[14] != "" :
							activity_json["enrolment_enddate"] = data[14]
						if data[15] != "" :
							activity_json["balloting"] = data[15]
						if data[16] != "" :
							activity_json["enrolment_remain_startdate"] = data[16]
						if data[17] != "" :
							activity_json["enrolment_remain_enddate"] = data[17]
						if data[18] != "" :
							activity_json["created_at"] = data[18]
						# mongodb
						if storage_mongo:
							Mongo.save(act_table, activity_json, {'id': data[0]})
						# mysql
						if storage_mysql:
							success = mySQL.upsert(act_table, activity_json)
						storage_file_json.append(activity_json);


						data = []
						content = content[end+5:]

				i+=1
			m=month+1
		#filre storage
		if storage_file :
			filename=storage_dir+act_table+".json"
			if os.path.exists(filename):
				with open(filename, 'w') as outfile:
					os.chmod(filename, 777)
					json.dump(storage_file_json, outfile, indent=8)
			else:
				with open(filename, 'w') as outfile:
					os.chmod(filename, 777)
					json.dump(storage_file_json, outfile, indent=8)



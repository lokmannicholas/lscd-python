from datetime import date



def todate(_date):#d/m
	dateformate=_date.split('/')
	day=dateformate[0]
	month=dateformate[1]
	if date.today().month>month and 1<= month and month<=6 :
		year=date.today().year+1
	elif date.today().month<month and 1<= date.today().month and date.today().month<=6:
		year=date.today().year-1
	else:
		year=date.today().year
	todate='%s-%s-%s' %(year,month,day)
	return todate


import csv
import MySQLdb

mydb = MySQLdb.connect(host='127.0.0.1',user='root',passwd='',db='Project')
cursor = mydb.cursor()
csv_data = csv.reader(file('Company.csv'))
i = 0
for row in csv_data:
	for i in range(0,len(row)):
		if row[i] == '' or row[i] == '-':
			row[i] = None
	data = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]]
	#print data
	sql = 'INSERT INTO company(`Symbol`,`Company`,`Market`,`Industry`,`Sector`,`MySector`,`ESector`,`SET50`,`SET100`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
	cursor.execute(sql,data)
	mydb.commit()
cursor.close()
print "Done"

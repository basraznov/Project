import csv
import pymysql
import init as it

mydb = pymysql.connect(host=it.hostip,user=it.userdatebase,passwd=it.passdatabase,db=it.datebasename)
cursor = mydb.cursor()
csv_data = csv.reader(open('../22022018.csv'))
i = 0
for row in csv_data:
	# k = '20'+row[0][6]+row[0][7]+'-'+row[0][3]+row[0][4]+'-'+row[0][0]+row[0][1]
	# for x in range(0,len(row)):
	# 	print(x,row[x])
	for i in range(0,len(row)):
		if row[i] == '':
			row[i] = None
		if row[i] == '-':
			row[i] = None
	if row[10] != '-' and row[10] != '' and row[10] != None or row[11] != '-' and row[11] != '' and row[11] != None:
		row[10] = row[10].replace(',', '')
	data = ['2018-02-22',row[0],row[2],row[3],row[4],row[5],row[7],row[10],row[11]]
	if row[0] == None:
		continue
	print(data)
	sql = 'INSERT INTO trade(`Date`,`Symbol`,`Open`,`High`,`Low`,`Last`,`ChPer`,`Volumn`,`Money`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
	cursor.execute(sql,data)
	mydb.commit()
cursor.close()

print ("Done")

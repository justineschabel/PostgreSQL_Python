import csv
import os
import glob
import psycopg2
import sys

# in order to figure out how to read in all of the .csv files that are in the directory
# we used this stackoverflow post for help:
# https://stackoverflow.com/questions/9234560/find-all-csv-files-in-a-directory-using-python

# primary help with using postgres:
# https://pythonspot.com/python-database-postgresql/

# used to figure out how to use command-line arguments in python and shellscript: n
# https://unix.stackexchange.com/questions/31414/how-can-i-pass-a-command-line-argument-into-a-shell-script
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
try:
	directory = sys.argv[1]
except:
	directory = os.getcwd()

try:
	conn = psycopg2.connect("dbname=FakeUData")
except:
	print("cant connect!")

cur = conn.cursor()

createTables = [
	"""CREATE TABLE courses (
		cid VARCHAR(30) NOT NULL,
		term VARCHAR(30) NOT NULL,
		subj VARCHAR(30) NOT NULL,
		crse VARCHAR(30) NOT NULL,
		sec VARCHAR(30) NOT NULL,
		unitRange VARCHAR(30) NOT NULL,
		PRIMARY KEY (cid, term, subj, crse, sec)
		);""",

	"""CREATE TABLE meetings (
		instructors VARCHAR(60),
		type VARCHAR(30),
		days VARCHAR(10),
		tim VARCHAR(30),
		build VARCHAR(10),
		room VARCHAR(10),
		cid VARCHAR(15),
		term VARCHAR(15),
		subj VARCHAR(30),
		PRIMARY KEY (cid, term, days, tim, build, room)
		);""" ,

		"""CREATE TABLE students (
	    seat VARCHAR(10),
		sid VARCHAR(60)NOT NULL,
		surname VARCHAR(30),
		prefname VARCHAR(30),
		level VARCHAR(30),
		units VARCHAR(30),
		class VARCHAR(15),
		major VARCHAR(10),
		grade VARCHAR(15),
		status VARCHAR(60),
		email VARCHAR(50),
		sec VARCHAR(30) ,
		term VARCHAR(10)NOT NULL,
		cid VARCHAR(10) NOT NULL,
		PRIMARY KEY (sid, term, sec, cid)
	);""",

		"""CREATE TABLE grades (
		grade VARCHAR(10),
		value VARCHAR(30),
		units VARCHAR(30),
		gpa VARCHAR(30),
		PRIMARY KEY (grade, value, units)
	);"""
]

for query in createTables:
		cur.execute(query)

def makestr(bfl):
    bfs = ""
    for i in range(0,len(bfl)):
        mystr = "("
        for index in range(0,len(bfl[i])-1):
            mystr += '\'' + bfl[i][index] + '\'' + ', '
        mystr += '\'' + bfl[i][len(bfl[i])-1] + '\''
        mystr += ')'+ ', '
        bfs += mystr
    bfs = bfs[:-2]
    return bfs


os.chdir(directory)
csvFiles = glob.glob('**.csv')

for file in csvFiles:
	with open(file, 'rb') as f:
		#used to check for duplicates in summer courses
		crs = []

		data = [row for row in csv.reader(f.read().splitlines())]

		courses = []
		students = []
		meetings =[]

		cid = ''
		term = ''
		crse = ''
		sec = ''
		units = ''
		subj = ''

		index = 0
		while index < len(data):
			if data[index][0] == 'CID':
				index += 1
				while index < len(data) and  data[index] != ['']:
					cid = data[index][0]
					term = data[index][1]
					subj = data[index][2]
					crse = data[index][3]

					if [cid, term, subj, crse] in crs:
						data[index][1] = data[index][1] + '-02'
						term = data[index][1]

					crs.append([cid, term, subj, crse])

					sec = data[index][4]
					units = data[index][5]
					course = data[index]
					courses.append(course)
					index += 1

			elif data[index][0] == 'INSTRUCTOR(S)':
				index += 1
				while index < len(data) and  data[index] != ['']:
					data[index][0] = data[index][0].replace('\'', '\'\'')
					meeting = data[index]
					meeting.append(cid)
					meeting.append(term)
					meeting.append(subj)
					meetings.append(meeting)
					index += 1


			elif data[index][0] == 'SEAT':
				index += 1
				while  index < len(data) and data[index] != [''] :
					data[index][10]= data[index][10].replace('\'', '\'\'')
					data[index][2] = data[index][2].replace('\'', '\'\'')
					data[index][3] = data[index][3].replace('\'', '\'\'')
					student = data[index]
					if student[5] == '':
						student[5] = '0.0'
					student.append(sec)
					student.append(term)
					student.append(cid)
					students.append(student)
					index += 1


			else:
				index += 1

	sqlCourses = 'INSERT INTO courses VALUES ' + makestr(courses)+ ';'
	sqlMeetings = 'INSERT INTO meetings VALUES ' + makestr(meetings) + 'ON CONFLICT DO NOTHING ' + ';'
	sqlStudents = 'INSERT INTO students VALUES ' + makestr(students) + ';'

	cur.execute(sqlCourses)
	cur.execute(sqlMeetings)
	cur.execute(sqlStudents)


# grades_ =[('A+',4.0), ('A', 4.0),('A-', 3.7),('B+', 3.3),('B', 3.0), ('B-', 2.7),('C+', 2.3),('C', 2.0), ('C-', 1.7),('D+', 1.3),('D', 1.0),
# ('D-', 0.7),('F', 0.0)]
# grades = []
# for grade in grades_:
# 	for i in range(0,6):
# 		list = (grade[0], grade[1], i, grade[1]*i)
# 		grades.append(list)
# print(grades)
#I used the above code to generate the list below
grades = """('A+', 4.0, 0, 0.0), ('A+', 4.0, 1, 4.0), ('A+', 4.0, 2, 8.0), ('A+', 4.0, 3, 12.0), ('A+', 4.0, 4, 16.0), ('A+', 4.0, 5, 20.0),
 ('A', 4.0, 0, 0.0), ('A', 4.0, 1, 4.0), ('A', 4.0, 2, 8.0), ('A', 4.0, 3, 12.0), ('A', 4.0, 4, 16.0), ('A', 4.0, 5, 20.0), ('A-', 3.7, 0, 0.0),
 ('A-', 3.7, 1, 3.7), ('A-', 3.7, 2, 7.4), ('A-', 3.7, 3, 11.100000000000001), ('A-', 3.7, 4, 14.8), ('A-', 3.7, 5, 18.5), ('B+', 3.3, 0, 0.0),
 ('B+', 3.3, 1, 3.3), ('B+', 3.3, 2, 6.6), ('B+', 3.3, 3, 9.899999999999999), ('B+', 3.3, 4, 13.2), ('B+', 3.3, 5, 16.5), ('B', 3.0, 0, 0.0),
  ('B', 3.0, 1, 3.0), ('B', 3.0, 2, 6.0), ('B', 3.0, 3, 9.0), ('B', 3.0, 4, 12.0), ('B', 3.0, 5, 15.0), ('B-', 2.7, 0, 0.0), ('B-', 2.7, 1, 2.7),
  ('B-', 2.7, 2, 5.4), ('B-', 2.7, 3, 8.100000000000001), ('B-', 2.7, 4, 10.8), ('B-', 2.7, 5, 13.5), ('C+', 2.3, 0, 0.0), ('C+', 2.3, 1, 2.3),
  ('C+', 2.3, 2, 4.6), ('C+', 2.3, 3, 6.8999999999999995), ('C+', 2.3, 4, 9.2), ('C+', 2.3, 5, 11.5), ('C', 2.0, 0, 0.0), ('C', 2.0, 1, 2.0),
  ('C', 2.0, 2, 4.0), ('C', 2.0, 3, 6.0), ('C', 2.0, 4, 8.0), ('C', 2.0, 5, 10.0), ('C-', 1.7, 0, 0.0), ('C-', 1.7, 1, 1.7), ('C-', 1.7, 2, 3.4),
  ('C-', 1.7, 3, 5.1), ('C-', 1.7, 4, 6.8), ('C-', 1.7, 5, 8.5), ('D+', 1.3, 0, 0.0), ('D+', 1.3, 1, 1.3), ('D+', 1.3, 2, 2.6), ('D+', 1.3, 3, 3.9000000000000004),
  ('D+', 1.3, 4, 5.2), ('D+', 1.3, 5, 6.5), ('D', 1.0, 0, 0.0), ('D', 1.0, 1, 1.0), ('D', 1.0, 2, 2.0), ('D', 1.0, 3, 3.0), ('D', 1.0, 4, 4.0), ('D', 1.0, 5, 5.0),
  ('D-', 0.7, 0, 0.0), ('D-', 0.7, 1, 0.7), ('D-', 0.7, 2, 1.4), ('D-', 0.7, 3, 2.0999999999999996), ('D-', 0.7, 4, 2.8), ('D-', 0.7, 5, 3.5), ('F', 0.0, 0, 0.0),
  ('F', 0.0, 1, 0.0), ('F', 0.0, 2, 0.0), ('F', 0.0, 3, 0.0), ('F', 0.0, 4, 0.0), ('F', 0.0, 5, 0.0) """


sqlGrades = 'INSERT INTO grades VALUES ' + grades + ';'
cur.execute(sqlGrades)
conn.commit()
#used to help with iterating over arrays in python:
#http://www.diveintopython.net/file_handling/for_loops.html

cur.close()
conn.close()

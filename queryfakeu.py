import psycopg2
import collections
try:
	conn = psycopg2.connect("dbname=FakeUData")
except:
	print("cant connect!")

cur = conn.cursor()


def makestr2(bfl):
    bfs = ""
    for i in range(0,len(bfl)):
        mystr = "("
        for index in range(0,len(bfl[i])-1):
            mystr += '\'' + str(bfl[i][index]) + '\'' + ', '
        mystr += '\'' + str(bfl[i][len(bfl[i])-1]) + '\''
        mystr += ')'+ ', '
        bfs += mystr
    bfs = bfs[:-2]
    return bfs

def q3a():
	t = """SELECT sum(c) FROM (SELECT count(sid) c
	FROM students
	group by sid,term) q"""
	cur.execute(t)
	total = cur.fetchall()
	q3 = """
	SELECT count(c), c FROM(
	SELECT sum(cast(units as float)) c
	FROM students natural join courses
	WHERE subj in ('ABC', 'DEF')
	GROUP BY sid, term) q group by c order by c;
	"""
	cur.execute(q3)
	all = cur.fetchall()
	print("Query 3A:")
	for element in all:
		if element[1] <= 20 and element[1] != 0:
	 		print(" Units: ", element[1], " Percentage: ", round(float(element[0])/int(total[0][0])*100,4))

def q3b():
	findMaxInstrGPA = """
	SELECT * FROM
	(SELECT instructors, (sum(cast(gpa AS FLOAT))/(sum(cast(units AS FLOAT))))AS instrGPA
	FROM meetings NATURAL JOIN students NATURAL JOIN grades
	GROUP BY instructors) t1
	NATURAL JOIN
	(SELECT max(instrGPA) as instrGPA FROM
	(SELECT instructors, (sum(cast(gpa AS FLOAT))/(sum(cast(units AS FLOAT))))AS instrGPA
	FROM meetings NATURAL JOIN students NATURAL JOIN grades
	GROUP BY instructors) t) t2;
	"""

	findMinInstrGPA = """
	SELECT * FROM
	(SELECT instructors, (sum(cast(gpa AS FLOAT))/(sum(cast(units AS FLOAT))))AS instrGPA
	FROM meetings NATURAL JOIN students NATURAL JOIN grades
	GROUP BY instructors) t1
	NATURAL JOIN
	(SELECT min(instrGPA) as instrGPA FROM
	(SELECT instructors, (sum(cast(gpa AS FLOAT))/(sum(cast(units AS FLOAT))))AS instrGPA
	FROM meetings NATURAL JOIN students NATURAL JOIN grades
	GROUP BY instructors) t) t2;
	"""
	cur.execute(findMaxInstrGPA)
	easiestInstr = cur.fetchall()

	cur.execute(findMinInstrGPA)
	hardestInstr = cur.fetchall()

	print("Query 3B:")
	print('\n\nEasiest Instructors:')
	for i in easiestInstr:
		print(i)

	print('\n\nHardest Instructors:')
	for i in hardestInstr:
		print(i)

def q3c():

	q3 = """
		SELECT avg(g), u from (
		SELECT g, u from(
		(SELECT g, u FROM (
		SELECT s1.sid, s1.term, sum(cast(s1.gpa as FLOAT)) AS g, sum(cast(s1.units as FLOAT)) AS u
		FROM (students natural join grades) as s1
		GROUP BY s1.sid, s1.term
		ORDER BY u) f)
		fu
		natural join
		(SELECT u FROM (
		SELECT s1.sid, s1.term, sum(cast(s1.gpa as FLOAT)) AS g, sum(cast(s1.units as FLOAT)) AS u
		FROM (students natural join grades) as s1
		GROUP BY s1.sid, s1.term
		ORDER BY u) f2
		group by u
		) fu2
		)t ) a
		group by u limit 21
		;
	"""

	cur.execute(q3)
	all = cur.fetchall()
	gpas = []
	for i in range(1,len(all)):
		gpas.append((all[i][1], round(float(all[i][0])/all[i][1], 2)))
	print("Query 3C:")
	print("Average GPA based on the number of units taken")
	print(gpas)


def q3d():
	findHighestPassRateCourses = """
	SELECT * FROM (
	(SELECT t1.subj as subj, t1.crse as crse, CAST (CAST(numPass AS float)/CAST(numSt as float) AS float) AS passRate
	    FROM (SELECT count(sid) as numPass, subj, crse
	        FROM courses NATURAL JOIN students
	        WHERE students.grade IN ('A+', 'A', 'A-', 'B+','B', 'B-', 'C+', 'C', 'C-', 'P')
	        GROUP BY(subj, crse)) as t1 NATURAL JOIN
	        (SELECT count(sid) as numSt, subj, crse
	        FROM courses NATURAL JOIN students
	        WHERE students.grade IN ('A+', 'A', 'A-', 'B+','B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'NP', 'NS', 'P')
	        GROUP BY(subj, crse)) as t2) a
	  NATURAL JOIN
	(SELECT MAX(passRate) as passRate FROM(
	  SELECT t1.subj as subj, t1.crse as crse, CAST (CAST(numPass AS float)/CAST(numSt as float) AS float) AS passRate
	    FROM (SELECT count(sid) as numPass, subj, crse
	        FROM courses NATURAL JOIN students
	        WHERE students.grade IN ('A+', 'A', 'A-', 'B+','B', 'B-', 'C+', 'C', 'C-', 'P')
	        GROUP BY(subj, crse)) as t1 NATURAL JOIN
	        (SELECT count(sid) as numSt, subj, crse
	        FROM courses NATURAL JOIN students
	        WHERE students.grade IN ('A+', 'A', 'A-', 'B+','B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'NP', 'NS', 'P')
	        GROUP BY(subj, crse)) as t2) pr) b);
	"""

	findLowestPassRateCourses = """
	SELECT * FROM (
	(SELECT t1.subj as subj, t1.crse as crse, CAST (CAST(numPass AS float)/CAST(numSt as float) AS float) AS passRate
	    FROM (SELECT count(sid) as numPass, subj, crse
	        FROM courses NATURAL JOIN students
	        WHERE students.grade IN ('A+', 'A', 'A-', 'B+','B', 'B-', 'C+', 'C', 'C-', 'P')
	        GROUP BY(subj, crse)) as t1 NATURAL JOIN
	        (SELECT count(sid) as numSt, subj, crse
	        FROM courses NATURAL JOIN students
	        WHERE students.grade IN ('A+', 'A', 'A-', 'B+','B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'NP', 'NS', 'P')
	        GROUP BY(subj, crse)) as t2) a
	  NATURAL JOIN
	(SELECT MIN(passRate) as passRate FROM(
	  SELECT t1.subj as subj, t1.crse as crse, CAST (CAST(numPass AS float)/CAST(numSt as float) AS float) AS passRate
	    FROM (SELECT count(sid) as numPass, subj, crse
	        FROM courses NATURAL JOIN students
	        WHERE students.grade IN ('A+', 'A', 'A-', 'B+','B', 'B-', 'C+', 'C', 'C-', 'P')
	        GROUP BY(subj, crse)) as t1 NATURAL JOIN
	        (SELECT count(sid) as numSt, subj, crse
	        FROM courses NATURAL JOIN students
	        WHERE students.grade IN ('A+', 'A', 'A-', 'B+','B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F', 'NP', 'NS', 'P')
	        GROUP BY(subj, crse)) as t2) pr) b);
	"""

	cur.execute(findHighestPassRateCourses)
	highPass = cur.fetchall()
	print("Query 3D:")
	print('\n\nCourse(s) with highest pass rates: ')
	for i in highPass:
		print(i)

	cur.execute(findLowestPassRateCourses)
	lowPass = cur.fetchall()
	print('\n\nCourse(s) with lowest pass rates: ')
	for i in lowPass:
		print(i)

def q3e():
	q2 = """
	SELECT m1.subj, m1.crse, m2.subj, m2.crse
	from (select instructors, term, subj, days, tim, build, room, crse
			from meetings natural join courses
			where build NOT IN ('')) as m1
			cross join
			(select instructors, term, subj, days, tim, build, room, crse
			from meetings natural join courses
			where build NOT IN ('')) AS m2
	where m1.subj <> m2.subj and m1.days = m2.days and m1.tim = m2.tim and m1.build = m2.build and m1.room = m2.room and m1.instructors = m2.instructors and m1.term = m2.term
		group by (m1.subj, m1.crse, m2.subj, m2.crse)
		ORDER BY m1.subj, m1.crse;
		"""
	cur.execute(q2)
	subjcrse = cur.fetchall()
	check = []
	for tuple_  in subjcrse:
		reverse = tuple([tuple_[2], tuple_[3], tuple_[0], tuple_[1]])
		if (tuple_ not in check) and (reverse not in check):
			check.append(tuple_)
	print("Query 3E:")
	print(check)

def q3f():
	findMBA = """
	SELECT * FROM
	(SELECT max(majorPerfabc) AS majorPerfabc FROM (
	  SELECT major, (sum(cast(gpa AS FLOAT))/(sum(cast(units AS FLOAT)))) AS majorPerfabc
	  FROM (students NATURAL JOIN courses NATURAL JOIN grades)
	  WHERE courses.subj = 'ABC' GROUP BY major) AS t) t1
	NATURAL JOIN
	(SELECT major, (sum(cast(gpa AS FLOAT))/(sum(cast(units AS FLOAT)))) AS majorPerfabc
	  FROM (students NATURAL JOIN courses NATURAL JOIN grades)
	  WHERE courses.subj = 'ABC' GROUP BY major) t2;
	"""

	findMWA = """
	SELECT * FROM
	(SELECT min(majorPerfabc) AS majorPerfabc FROM (
	  SELECT major, (sum(cast(gpa AS FLOAT))/(sum(cast(units AS FLOAT)))) AS majorPerfabc
	  FROM (students NATURAL JOIN courses NATURAL JOIN grades)
	  WHERE courses.subj = 'ABC' GROUP BY major) AS t) t1
	NATURAL JOIN
	(SELECT major, (sum(cast(gpa AS FLOAT))/(sum(cast(units AS FLOAT)))) AS majorPerfabc
	  FROM (students NATURAL JOIN courses NATURAL JOIN grades)
	  WHERE courses.subj = 'ABC' GROUP BY major) t2;
	"""

	findMBD = """
	SELECT * FROM
	(SELECT max(majorPerfabc) AS majorPerfabc FROM (
	  SELECT major, (sum(cast(gpa AS FLOAT))/(sum(cast(units AS FLOAT)))) AS majorPerfabc
	  FROM (students NATURAL JOIN courses NATURAL JOIN grades)
	  WHERE courses.subj = 'DEF' GROUP BY major) AS t) t1
	NATURAL JOIN
	(SELECT major, (sum(cast(gpa AS FLOAT))/(sum(cast(units AS FLOAT)))) AS majorPerfabc
	  FROM (students NATURAL JOIN courses NATURAL JOIN grades)
	  WHERE courses.subj = 'DEF' GROUP BY major) t2;
	"""

	findMWD = """
	SELECT * FROM
	(SELECT min(majorPerfabc) AS majorPerfabc FROM (
	  SELECT major, (sum(cast(gpa AS FLOAT))/(sum(cast(units AS FLOAT)))) AS majorPerfabc
	  FROM (students NATURAL JOIN courses NATURAL JOIN grades)
	  WHERE courses.subj = 'DEF' GROUP BY major) AS t) t1
	NATURAL JOIN
	(SELECT major, (sum(cast(gpa AS FLOAT))/(sum(cast(units AS FLOAT)))) AS majorPerfabc
	  FROM (students NATURAL JOIN courses NATURAL JOIN grades)
	  WHERE courses.subj = 'DEF' GROUP BY major) t2;
	"""

	cur.execute(findMBA)
	majorBestABC = cur.fetchall()
	print("Query 3F:")
	print('\n\nmajorBestABC:')
	for i in majorBestABC:
		print i

	cur.execute(findMWA)
	majorWorstABC = cur.fetchall()
	print('\n\nmajorWorstABC:')
	for i in majorWorstABC:
		print i

	cur.execute(findMBD)
	majorBestDEF = cur.fetchall()
	print('\n\nmajorBestDEF:')
	for i in majorBestDEF:
		print i

	cur.execute(findMWD)
	majorWorstDEF = cur.fetchall()
	print('\n\nmajorWorstDEF:')
	for i in majorWorstDEF:
		print i


def q3g():
	q3 = """
	SELECT 	count(*) c, m1.major
	from (select sid, major, term
			from students) as m1
			cross join
		(select sid, major, term
					from students) as m2
	where m1.sid = m2.sid and m1.major <> m2.major and m1.major not like 'ABC%' and m2.major like 'ABC%' and m1.term < m2.term
	group by m1.major
	order by c
		"""
	cur.execute(q3)
	majors = cur.fetchall()
	totaltransfers = 0
	for item in majors:
		totaltransfers += item[0]


	answer = majors[-5:]
	print("Query 3G:")
	print("Rank is from highest number of transfers(1) to the lowest(5).")
	for t in range(len(answer)-1,-1,-1):
		print("Rank ", 5-t, answer[t][1])

	print("Percentage of students that transferred from one major to ABC")
	for t in range(len(answer)-1,-1,-1):
		print("Major: ", answer[t][1], " Percentage: ", float(answer[t][0])/totaltransfers)

def q3h():
	q3 = """
	SELECT 	count(*) c, m1.major
	from (select sid, major, term
			from students) as m1
			cross join
		(select sid, major, term
					from students) as m2
	where m1.sid = m2.sid and m1.major <> m2.major and m1.major not like 'ABC%' and m2.major like 'ABC%' and m1.term > m2.term
	group by m1.major
	order by c
		"""
	cur.execute(q3)
	majors = cur.fetchall()
	totaltransfers = 0
	for item in majors:
		totaltransfers += item[0]

	print("Query 3h:")
	answer = majors[-5:]
	print("Rank is from highest number of transfers(1) to the lowest(5).")
	for t in range(len(answer)-1,-1,-1):
		print("Rank ", 5-t, answer[t][1])

	print("Percentage of students that transferred from ABC to Top Majors")
	for t in range(len(answer)-1,-1,-1):
		print("Major: ", answer[t][1], " Percentage: ", float(answer[t][0])/totaltransfers)

q3a()
q3b()
q3c()
q3d()
q3e()
q3f()
q3g()
q3h()


conn.commit()
cur.close()
conn.close()

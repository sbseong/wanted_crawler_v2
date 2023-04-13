# 디렉토리 내부 정보 받아서 db merge

import os
import sqlite3
from datetime import datetime
import pandas as pd

# 해당 폴더 내의 db 파일의 리스트를 받아서 머지합니다. 다른 파일들은 제거해주세요.
dir_info = input(f"원하시는 폴더명을 입력하세요 :")

# 리스트로 정보 확인 : https://pynative.com/python-list-files-in-a-directory/
tmp = os.listdir(dir_info)

print("List of DBs\n")

# DB을 합쳐서 저장할 new db 를 제작합니다. 
# 제작하는 DB의 명칭을 폴더이름에서 가져옵니다.
Dbase = "{}_auto_merge.db".format(dir_info)
co = sqlite3.connect(Dbase)
ccc = co.cursor()
ccc.execute('''
CREATE VIRTUAL TABLE IF NOT EXISTS JDinfo 
USING FTS3(JD_id, CoName, Jikmu, JobToDo, requirement, preferential, walfare, skills, close_date, location, url);
''')
co.commit()

# DB들을 불러다가 신규 DB안에 Concat을 시도합니다.
try:
	for i in range(1,3):
		globals()["db_{}".format(str(i))] = sqlite3.connect(dir_info + '/' + str(tmp[i]))
		print("Connected to SQLite \n")
		print (globals()["db_{}".format(str(i))])
		for row in globals()["db_{}".format(str(i))].execute("select * FROM JDinfo"):
		    # print (row[1])
			ccc.execute("INSERT INTO JDinfo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (row[0],row[1],row[2],row[3],row[4],row[5], row[6], row[7], row[8], row[9], row[10]))
			co.commit()

	# for row in db_2.execute("select * FROM JDinfo"):
	#     print (row[1])
	#     ccc.execute("INSERT INTO JDinfo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (row[0],row[1],row[2],row[3],row[4],row[5], row[6], row[7], row[8], row[9], row[10]))
	#     co.commit()

except:
    print("DB Concat에 실패")
    pass

save_date = datetime.today().strftime("%Y%m%d_%H%M")
filename = "{}_folder_{}_auto_merge.csv"
nameVar = [str(dir_info), str(save_date)]
try:
	conn = sqlite3.connect("{}_auto_merge.db".format(dir_info), isolation_level=None,
                       detect_types=sqlite3.PARSE_COLNAMES)
	db_df = pd.read_sql_query("SELECT * FROM JDinfo", conn)
	db_df.to_csv(filename.format(*nameVar), index=False)
	conn.close()
except:
    print("DB to csv 에러")
    pass
# try: 
# 	# Get the contents of a table
# 	b_cursor.execute('SELECT * FROM "JDinfo"')
# 	output = b_cursor.fetchall()   # Returns the results as a list.

# 	# Insert those contents into another table.
# 	for row in output:
# 	    a_cursor.execute('INSERT INTO JDinfo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row)
# except sqlite3.Error as error:
# 	print("DB concat 실패 :", error)
# 	pass

# Cleanup
db_1.commit()
print("DB 저장 끝~~!")


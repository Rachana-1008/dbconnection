import pymysql as mq
conn = mq.connect(host='localhost',password='root',user='root',database='datab1')

mycursor = conn.cursor()
print("connection done successfully")

# mycursor.execute("create Database datab1")
# print("database created sucessfully")

# mycursor.execute("""CREATE TABLE employee(
#                  id int primary key not null,
#                  emp_name VARCHAR(50), emp_no int )""")
# print("table is created sucessfully")

# mycursor.execute("insert into employee values('4','samiksha','25')")
# conn.commit()
# print("record inserted")

# update_query = "UPDATE employee SET emp_name = 'ankita' WHERE id=4"
# mycursor.execute(update_query)
# conn.commit()
# mycursor.close()
# conn.close()
# print("recors updated")

delete_query = "DELETE FROM employee WHERE id=3"
mycursor.execute(delete_query)
conn.commit()
mycursor.close()
conn.close()
print("recodrs deleted")
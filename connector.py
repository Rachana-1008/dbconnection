import pymysql as mq
conn = mq.connect(host="localhost",password='root',user='root',database='db1')

mycursor=conn.cursor()
print("connection done successfull")

# mycursor.execute("create database db1")
# print("database create successfull")

# mycursor.execute("""create table employee(
#                  id int primary key not null,
#                  emp_name VARCHAR(50),
#                  emp_no int)"""
# )
# print("table created successfully")

# mycursor.execute("insert into employee values('5','anku','31')")
# conn.commit()
# print("record inserted")

# update_query ="UPDATE employee SET emp_name = 'bansi' WHERE  id = 1"
# mycursor.execute(update_query)
# conn.commit()
# mycursor.close()
# conn.close()
# print("record updated")


delete_query ="DELETE FROM employee  WHERE  id = 2"
mycursor.execute(delete_query)
conn.commit()
mycursor.close()
conn.close()
print("record deleted")

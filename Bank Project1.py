
import pymysql as mq   #Python libraries for working with MySQL databases 
import random #generating random values
import uuid
from prettytable import PrettyTable #formatting tables 
from decimal import Decimal #handling decimal numbers


db=mq.connect(host='localhost',user='root',password='root',database='bank')
cursorobj=db.cursor()
print("Connected")

# # Creation on database
# bank="create database bank"
# cursorobj.execute(bank)
# print("Database Created")

# create table
# cursorobj.execute("create table admin(admin_id bigint auto_increment key ,f_name varchar(50) , l_name varchar(50) , password varchar(50) unique key);")
# cursorobj.execute("create table user(user_id bigint auto_increment key , f_name varchar(50) , l_name varchar(50) , balance bigint , password varchar(10) unique key , account_no bigint unique key);")
# cursorobj.execute("create table history(id bigint , f_name varchar(50) , l_name varchar(50) , trans_type varchar(100) ,trans_amount bigint , account_no bigint , balance bigint ,remark varchar(100));")
# cursorobj.execute("CREATE TABLE IF NOT EXISTS history(id INT AUTO_INCREMENT PRIMARY KEY,user_id INT,remarks VARCHAR(255),amount DECIMAL(10, 2),transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
# db.commit()

def generate_unique_id():
    return str(uuid.uuid4())
    #return random.randint(1,99)


def generate_unique_account_number():
    return random.randint(10000,99999999999)

# function for admin()
def admin():
    admin_id = int(input("Enter an admin ID: "))
    password = input("Enter a Password: ")
    cursorobj.execute("SELECT * FROM admin WHERE admin_id = %s AND password = %s", (admin_id, password))
    admin=cursorobj.fetchone()
    if admin:
        print("Admin login Sucessfully")
        return admin
    else:
        print("Invalid ID or Password..")

# function for admin creation    
def create_admin():
    print("------------ CREATE NEW ADMIN ACCOUNT ----------")
    admin_id=generate_unique_id()
    f_name = input("Enter First Name: ")
    l_name = input("Enter Last Name: ")
    password = input("Enter Password: ")
    # insert into admin table
    

    cursorobj.execute("INSERT INTO admin (f_name, l_name, password) VALUES ( %s, %s, %s)", ( f_name, l_name, password))
    print("Admin Sucessfully Added...")
    db.commit()
    print(f"User Account Created with Account no :{admin_id} ")


# function for user login
def user():
    account_no = int(input("Enter Account No: "))
    password = input("Enter a Password: ")
    cursorobj.execute("SELECT * FROM user WHERE account_no = %s AND password = %s", (account_no, password))
    user =cursorobj.fetchone()
    if user:
        print("User login Sucessfully")
        return user
    else:
        print("Invalid ID or Password..")

# function for user creation    
def create_user():
    print("----------- CREATE NEW USER ACCOUNT --------")
    account_no= generate_unique_account_number()
    f_name = input("Enter First Name: ")
    l_name = input("Enter Last Name: ")
    balance=float(input("Enter Opening Account Amount:"))
    password = input("Enter Password: ")
    # insert into user table
    cursorobj.execute("INSERT INTO user ( f_name, l_name, balance, password, account_no) VALUES (%s, %s, %s, %s, %s)", ( f_name, l_name, balance, password, account_no))
    print("User Sucessfully Added...")
    db.commit()
    print(f"User Account Created with Account no : {account_no}")

# function for display all users
def display_user():
    print("----------- ALL USER LIST -----------")
    cursorobj.execute("SELECT * from user")
    user = cursorobj.fetchall()
    table = PrettyTable()
    table.field_names = ["User ID", "First Name","Last Name" ,"Balance","Password","Account No"]
    for users in user:
        table.add_row(users)
    print(table)
    
    db.commit()

# function for deposite 
def deposite(user):
    cursorobj.execute("SELECT balance FROM user WHERE user_id = %s",(user[0],))
    balance1=cursorobj.fetchone()[0]

    userdeposite=Decimal(input("Enter Amount to Deposite : "))

    if userdeposite > 0:
        new_balance=Decimal(balance1 + userdeposite)
        update_balance(user[0],new_balance)
        print(f"Amount deposited Sucessfully.... New Balance : {new_balance:.2f}")
        update_transaction_history(user[0], "Deposited successfully", userdeposite)
    else:
        print("Invalid amount")

# function for update transaction 
def update_transaction_history(user_id, remarks, amount):
        
    cursorobj.execute(" INSERT INTO history (user_id, remarks, amount)VALUES (%s, %s, %s)",(user_id, remarks, amount))
    db.commit()
    print(f"Transaction history updated for user_id {user_id}")
        
# function for withdraw
def withdraw(user):
    cursorobj.execute("SELECT balance FROM user WHERE user_id = %s",(user[0],))
    balance1=cursorobj.fetchone()[0]

    userdeposite=Decimal(input("Enter Amount to Deposite : "))

    if userdeposite > 0:
        new_balance=Decimal(balance1 - userdeposite)
        update_balance(user[0],new_balance)
        print(f"Amount deposited Sucessfully.... New Balance : {new_balance:.2f}")
        update_transaction_history(user[0], "Withdraw successfully", userdeposite)

    else:
        print("Invalid amount")

# check balance
def check_balance(user):
    cursorobj.execute("SELECT balance FROM user WHERE user_id = %s", (user[0],))
    result = cursorobj.fetchone()

    if result is not None:
        new_balance = result[0]
        print(f"Your Balance: {new_balance:.2f}")
    else:
        print("User not found or balance data missing")

# function for update balance
def update_balance(user_id, new_balance):
    try:
        cursorobj.execute("UPDATE user SET balance = %s WHERE user_id =%s ",(new_balance,user_id))
        db.commit()
        print(f"Updating balance from user_id {user_id} to {new_balance:.2f}")
    except:
        print(f"Error UPdating Balance ")


# function for transaction history
def transaction_history(user):
    print("Transaction History")
    user_id = user[0]
    try:
        cursorobj.execute("SELECT his.transaction_date, his.remarks, his.amount, u.f_name, u.l_name, u.account_no, u.balance "
                       "FROM history his "
                       "JOIN user u ON his.user_id = u.user_id "
                       "WHERE u.user_id = %s", (user_id,))
        transactions = cursorobj.fetchall()

        table = PrettyTable()
        table.field_names = ["Transaction Date and Time", "Remarks", "Amount", "First Name", "Last Name", "Account No",]

        for transaction in transactions:
            table.add_row([transaction[0], transaction[1], transaction[2], transaction[3], transaction[4], transaction[5]])

        print(table)
    except :
        print(f"Error fetching transaction history")

# function for update user
def update():
  """Updates the user's details."""
  print("Update User Details")
  user_id = int(input("Enter the User ID to update: "))

  # Select the user's details from the database.
  cursorobj.execute("SELECT user_id, account_no, f_name, l_name, balance FROM user WHERE user_id = %s", (user_id,))
  user = cursorobj.fetchone()

  if user:
    # Display the user's details in a table.
    table = PrettyTable()
    table.field_names = ["User ID", "Account No", "First Name", "Last Name", "Balance"]
    table.add_row(user)
    print(table)

    # Ask the user to confirm if they want to update their account details.
    conf = input("Are you sure you want to update your account details?\n(y/n)\n")

    if conf == "y":
      # Get the new user details from the user.
      newf_name = input("Enter your new First Name: ")
      newl_name = input("Enter your New Last Name: ")
      new_balance = float(input("Enter the new balance: "))
      new_pas = input("Enter the new password: ")
      confnewpass = input("Confirm password: ")

      # Validate the new password.
      while True:
        if new_pas == confnewpass:
          print("Password changed successfully")
          break
        else:
          print("Password Not Same")

      # Update the user's details in the database.
      cursorobj.execute("UPDATE user SET f_name=%s, l_name=%s, balance=%s, password=%s WHERE user_id=%s",
                        (newf_name, newl_name, new_balance, new_pas, user_id))

      # Commit the changes to the database.
      db.commit()

      print("User details updated")
    else:
      print("Account update canceled.")
  else:
    print("User not found.")

# function for delete the user
def delete():
    print("Delete User Details")
    user_id = int(input("Enter the User ID to delete: "))

    cursorobj.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
    user = cursorobj.fetchone()

    if user is None:
        print("User not found.")
        return
    cursorobj.execute("DELETE FROM user WHERE user_id = %s" ,(user_id,))
    db.commit()
    print("User account deleted")



while True:
    print("---------------------------")
    print("Welcome to ICICI Bank")
    print("---------------------------")
    print("1. Admin ")
    print("2. User ")
    print("3. Exit ")
    ch=int(input("Enter your choice : "))

    if ch==1:
        print("------- ADMIN PANEL --------")
        print("1. Login Now ")
        print("2.Exit")
        admin_ch=int(input("Enter Choice : "))

        # Admin login
        if admin_ch==1:
            print("--------- ADMIN LOGIN PANEL -------")
            admin_data = admin()
            if admin_data:  # Check if admin login was successful
                while True:
                    print("-----------SELECT ANY OPERATION -----------")
                    print("1. CREATE ADMIN ACCOUNT")
                    print("2. CREATE USER ACCOUNT")
                    print("3. UPDATE USER DETAILS")
                    print("4. DELETE USER ACCOUNT")
                    print("5. SHOW USER DETAILS")
                    print("6. EXIT")
                    admin_ch = int(input("Enter Choice : "))
                    if admin_ch == 1:
                        create_admin()
                    elif admin_ch == 2:
                        create_user()
                    elif admin_ch == 3:
                        update()
                    elif admin_ch == 4:
                        delete()
                    elif admin_ch == 5:
                        display_user()
                    elif admin_ch == 6:
                        print("THANK YOU.....VISIT AGAIN")
                        break
                    else:
                        print("Invalid Selection")
                        exit()
        # Exit
        elif admin_ch==2:
            print(" ---------- EXIT --------")
            print("Thank You")
            continue

    elif ch == 2:
        print("-------- USER PANEL -------- ")
        print("1. Login")
        print("2. Exit")
    
        user_ch_input = input("Enter Choice: ")

        # Validate if the input is not empty
        if user_ch_input.strip():
            user_ch = int(user_ch_input)
            if user_ch == 1:
                print(" -------- USER LOGIN PANEL -------- ")
                user_data = user()
                if user_data:
                    while True:
                        print("---------------SELECT ANY OPERATION-----------------")
                        print("1. WITHDRAW")
                        print("2. DEPOSIT")
                        print("3. CHECK BALANCE")
                        print("4. TRANSACTION HISTORY")
                        print("5. EXIT")
                        user_choice_input = input("Enter Choice: ")

                        # Validate if the input is not empty
                        if user_choice_input.strip():
                            user_choice = int(user_choice_input)
                    
                            if user_choice == 1:
                                withdraw(user_data)
                            elif user_choice == 2:
                                deposite(user_data)
                            elif user_choice == 3:
                                check_balance(user_data)
                            elif user_choice == 4:
                                transaction_history(user_data)
                            elif user_choice == 5:
                                print("THANK YOU........VISIT AGAIN")
                                break
                            else:
                                print("Invalid selection")
                        else:
                            print("Invalid input. Please enter a choice.")
        else:
            print("Invalid input. Please enter a choice.")
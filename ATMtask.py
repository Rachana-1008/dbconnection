import pymysql as mq

conn = mq.connect(host='localhost', password='root', user='root', database='atm_db')

mycursor = conn.cursor()
print("Connection established successfully")


# mycursor.execute("create Database atm_db")
# print ("database created successfully")

# mycursor.execute('''
# CREATE TABLE users (
#     user_id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(50) ,
#     password VARCHAR(50),
#     balance DECIMAL(10, 2)
# )
# ''')
# print("Table 'users' created successfully")
# conn.commit()

def create_user():
    # Get username and password from the user
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    balance = 0.0

    mycursor.execute('''
    INSERT INTO users (username, password, balance) VALUES (%s, %s, %s)
    ''', (username, password, balance))

    conn.commit()

    print("User created successfully!")

def deposit(user_id,password):
    # Get deposit amount from the user
    amount = float(input("Enter deposit amount: "))

    mycursor.execute('''
    UPDATE users SET balance = balance + %s WHERE user_id = %s and password= %s
    ''', (amount, user_id,password))
    conn.commit()

    print(f"Deposit successful! Updated balance: {check_balance(user_id)}")

def withdraw(user_id):
    # Get deposit amount from the user
    amount = float(input("Enter withdraw amount: "))

    mycursor.execute('''
    UPDATE users SET balance = balance - %s WHERE user_id = %s
    ''', (amount, user_id))
    conn.commit()

    print(f"withdraw successful! Updated balance: {check_balance(user_id)}")    

def check_balance(user_id):
    mycursor.execute('''
    SELECT balance FROM users WHERE user_id = %s
    ''', (user_id,))
    balance = mycursor.fetchone()[0]
    return balance

while True:
    print("1. Create User")
    print("2. Deposit")
    print("3. withdraw")
    print("4. Check Balance")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        create_user()
    elif choice == '2':
        user_id = int(input("Enter your user ID: "))
        password = int(input("Enter your password: "))

        deposit(user_id,password)
    elif choice == '3':
        user_id = int(input("Enter your user ID: "))
        withdraw(user_id)
    elif choice == '4':
        user_id = int(input("Enter your user ID: "))
        print(f"Current balance: {check_balance(user_id)}")
    elif choice == '5':
        print("Exiting ATM. Thank you!")
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection
conn.close()

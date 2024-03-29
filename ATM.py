import mysql.connector
from getpass import getpass

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="atm"
)
cursor = conn.cursor()

# Create accounts table
cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    account_number INT PRIMARY KEY,
    pin INT,
    balance DECIMAL(10, 2)
)
''')
conn.commit()

# Function to create a new account
def create_account():
    pin = int(getpass("Enter your PIN: "))
    balance = float(input("Enter initial balance: "))

    cursor.execute('''
    INSERT INTO accounts (pin, balance) VALUES (%s, %s)
    ''', (pin, balance))
    conn.commit()

    print("Account created successfully!")

# Function to perform a withdrawal
def withdraw(account_number):
    amount = float(input("Enter withdrawal amount: "))

    cursor.execute('''
    UPDATE accounts SET balance = balance - %s WHERE account_number = %s
    ''', (amount, account_number))
    conn.commit()

    print(f"Withdrawal successful! Updated balance: {check_balance(account_number)}")

# Function to check account balance
def check_balance(account_number):
    cursor.execute('''
    SELECT balance FROM accounts WHERE account_number = %s
    ''', (account_number,))
    balance = cursor.fetchone()[0]
    return balance

# Main ATM loop
while True:
    print("1. Create Account")
    print("2. Withdraw")
    print("3. Check Balance")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        create_account()
    elif choice == '2':
        account_number = int(input("Enter your account number: "))
        withdraw(account_number)
    elif choice == '3':
        account_number = int(input("Enter your account number: "))
        print(f"Current balance: {check_balance(account_number)}")
    elif choice == '4':
        print("Exiting ATM. Thank you!")
        break
    else:
        print("Invalid choice. Please try again.")

# Close the database connection
conn.close()

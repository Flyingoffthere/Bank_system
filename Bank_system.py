import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS card (
id INTEGER,
number TEXT,
pin TEXT,
balance INTEGER DEFAULT 0)
""")
conn.commit()


class Card:
    def __init__(self):
        self.number = None
        self.PIN = None
        self.balance = None


def Luhn(num):
    new_num = num[:-1]
    checksum = 0
    for i in range(0, len(new_num)):
        if i % 2 == 0:
            if (2*int(new_num[i])) > 9:
                checksum += 2*int(new_num[i]) - 9
            else:
                checksum += 2*int(new_num[i])
        else:
            checksum += int(num[i])
    checksum += int(num[15])
    return (checksum % 10) == 0

def existence_of_card(num):
    cur.execute("SELECT number FROM card")
    numbers = [''.join(_) for _ in cur.fetchall()]
    conn.commit()
    for _ in numbers:
        if _ == num:
            return True
    return False


i = None

while i != 0:
    print('''1. Create an account
2. Log into account
0. Exit
    ''')
    i = int(input())

    if i == 1:
        card = Card()
        user_id = ''.join(str(random.randint(0, 9)) for i in range(0, 9))
        cur.execute("SELECT CAST(id as TEXT) FROM card")
        users_id = [''.join(_) for _ in cur.fetchall()]
        conn.commit()
        while user_id in users_id:
            user_id = ''.join(str(random.randint(0, 9)) for i in range(0, 9))
        if user_id in users_id:
            print('Sorry, there are not resources to create your card')
            break
        raw_number = '400000' + user_id
        r = ''
        for i in range(0, len(raw_number)):
            if i % 2 == 0:
                if int(2 * int(raw_number[i])) > 9:
                    a = int(2 * int(raw_number[i]))
                    a = a - 9
                    r += str(a)
                else:
                    r += str(2 * int(raw_number[i]))
            else:
                r += raw_number[i]
        raw_number = []
        for _ in r:
            raw_number.append(int(_))
        control_sum = sum(raw_number)
        if control_sum % 10 == 0:
            checksum = '0'
        else:
            checksum = str(10 - (control_sum % 10))
        card.number = '400000' + user_id + checksum
        card.PIN = ''.join(str(random.randint(0, 9)) for i in range(0, 4))
        card.balance = 0
        cur.execute(f'INSERT INTO card VALUES (CAST({user_id} AS INTEGER), {card.number}, {card.PIN}, {card.balance})')
        conn.commit()
        print(f'''Your card has been created
Your card number:
{card.number}
Your card PIN:
{card.PIN}
        ''')
    elif i == 2:
        print('Enter your card number:')
        num = input()
        print('Enter your PIN:')
        pin = input()
        r = 0
        cur.execute("SELECT number, pin FROM card")
        base = cur.fetchall()
        conn.commit()
        for _ in base:
            if _[0] == num and _[1] == pin:
                print("You have successfully logged in!")
                k = None
                while k != 0 or k != 2:
                    print('''1. Balance
2. Add income
3. Do transfer
4. Close account                    
5. Log out
0. Exit                    ''')
                    k = int(input())
                    if k == 1:
                        cur.execute(f'SELECT balance FROM card WHERE number = {num}')
                        b = cur.fetchone()[0]
                        conn.commit()
                        print(f'Balance: {b}')
                        continue
                    elif k == 2:
                        print('Enter income:')
                        income = int(input())
                        cur.execute(f'UPDATE card SET balance = balance + {income} WHERE number = {num}')
                        conn.commit()
                        print('Income was added!')
                        continue
                    elif k == 3:
                        print('Enter card number:')
                        receiver = input()
                        if num == receiver:
                            print("You can't transfer money to the same account!")
                            continue
                        elif existence_of_card(receiver) is False and Luhn(receiver) is True:
                            print('Such a card does not exist')
                            continue
                        elif not Luhn(receiver):
                            print('Probably you made a mistake in the card number. Please try again!')
                            continue
                        print('Enter how much money you want to transfer:')
                        amount = int(input())
                        cur.execute(f"SELECT balance FROM card WHERE number = {num}")
                        balance = cur.fetchone()[0]
                        conn.commit()
                        if amount > balance:
                            print('Not enough money!')
                            continue
                        else:
                            cur.execute(f"UPDATE card SET balance = {balance - amount} WHERE number = {num}")
                            conn.commit()
                            cur.execute(f"UPDATE card SET balance = balance + {amount} WHERE number = {receiver}")
                            conn.commit()
                            print('Success!')
                    elif k == 4:
                        cur.execute(f"DELETE FROM card WHERE number = {num}")
                        conn.commit()
                        print('The account has been closed!')
                        break
                    elif k == 5:
                        print('You have successfully logged out!')
                        break
                    elif k == 0:
                        i = 0
                        print('Bye!')
                        break
                    else:
                        print('Incorrect choice')
                        continue
            else:
                r += 1
        if r == len(base):
            print('Wrong card number or PIN!')
    elif i == 0:
        print('Bye!')
        break
    else:
        print('Incorrect choice')
        continue

conn.close()
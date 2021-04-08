import random
import sqlite3


class BankCard:

    def __init__(self):
        self.number_card = None
        self.pin_card = None
        self.balance = 0

    def luna(self):
        control_sum_list = []
        check_digit = 0
        for i in range(len(self.number_card)):
            if i % 2 == 0:
                check_digit_num = self.number_card[i]*2
                if check_digit_num > 9:
                    check_digit_num = check_digit_num - 9
                control_sum_list.append(check_digit_num)
            else:
                control_sum_list.append(self.number_card[i])
        control_sum = sum(control_sum_list)
        if control_sum % 10 != 0:
            check_digit = 10 - control_sum % 10
        return check_digit

    def generate_card_number(self):
        print("Your card has been created")
        self.number_card = ''
        for i in range(9):
            self.number_card = self.number_card + str(random.randint(0, 9))
        self.number_card = '400000' + self.number_card
        self.number_card = [int(i) for i in self.number_card]
        self.number_card = ''.join(str(i) for i in self.number_card) + str(self.luna())
        print("Your card number:\n" + self.number_card)
        self.pin_card = random.sample(range(9), 4)
        self.pin_card = ''.join(str(i) for i in self.pin_card)
        print("Your card PIN:\n" + self.pin_card)

    @staticmethod
    def get_identification(card_number, card_pin):
        conn = sqlite3.connect('card.s3db')
        cursor = conn.cursor()
        cursor.execute(f'''SELECT number, pin FROM card WHERE number = {card_number} AND pin = {card_pin};''')
        conn.commit()
        account = cursor.fetchall()
        if len(account) == 1:
            print("You have successfully logged in!")
            return account
        else:
            print("Such a card does not exist.")

    def get_balance(self, card_number, card_pin):
        conn = sqlite3.connect('card.s3db')
        cursor = conn.cursor()
        cursor.execute(f'''SELECT balance FROM card WHERE number = {card_number} AND pin = {card_pin};''')
        conn.commit()
        account = cursor.fetchall()
        return account

    def set_balanse(self, card_number, card_pin):
        conn = sqlite3.connect('card.s3db')
        cursor = conn.cursor()
        print('Enter income:')
        account = self.get_balance(card_number, card_pin)
        new_balance = str(int(input()) + int(account[0][0]))
        cursor.execute(f'''UPDATE card SET balance = {new_balance} WHERE number = {card_number} AND pin = {card_pin};''')
        conn.commit()
        print("Income was added!")

    def set_transfer(self, card_number, card_pin):
        conn = sqlite3.connect('card.s3db')
        cursor = conn.cursor()
        self.number_card = input("Transfer\nEnter card number:")
        last_num_card = self.number_card[-1]
        self.number_card = [int(i) for i in self.number_card[:-1]]
        check_digit = self.luna()
        if check_digit != int(last_num_card):
            print("Probably you made a mistake in the card number. Please try again!")
            return
        self.number_card = ''.join(str(i) for i in self.number_card) + last_num_card
        cursor.execute(f'''SELECT number, balance FROM card WHERE number = {self.number_card};''')
        conn.commit()
        account = cursor.fetchall()
        if len(account) == 0:
            print("Such a card does not exist.")
            return
        elif self.number_card == card_number:
            print("You can't transfer money to the same account!")
            return
        transfer_money = int(input("Enter how much money you want to transfer:\n"))
        cursor.execute(f'''SELECT balance FROM card WHERE number = {card_number};''')
        conn.commit()
        account_balance = cursor.fetchall()
        if transfer_money > int(account_balance[0][0]):
            print("Not enough money!")
            return
        cursor.execute(f'''UPDATE card SET balance = {transfer_money} WHERE number = {self.number_card};''')
        cursor.execute(f'''UPDATE card SET balance = {int(account_balance[0][0]) - int(transfer_money)} WHERE number = {card_number};''')
        conn.commit()

    def menu_account(self, card_number, card_pin):
        account = self.get_identification(card_number, card_pin)
        try:
            if len(account) == 1:
                while True:
                    print(
                        """
                            1. Balance
                            2. Add income
                            3. Do transfer
                            4. Close account
                            5. Log out
                            0. Exit
                        """
                    )
                    user = input()
                    if user == '0':
                        print("Bye")
                        exit()
                    if user == '1':
                        print(self.get_balance(card_number, card_pin)[0][0])
                    elif user == '2':
                        self.set_balanse(card_number, pin_card)
                    elif user == '3':
                        self.set_transfer(card_number, pin_card)
                    elif user == '4':
                        cursor.execute(f'''DELETE FROM card WHERE number = {card_number} AND pin = {pin_card}''')
                        conn.commit()
                        print("The account has been closed!")
                        break
                    else:
                        print("You have successfully logged out!")
                        break
        except TypeError:
            print("Wrong card number or PIN!")


conn = sqlite3.connect('card.s3db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS card (
id INTEGER,
number text,
pin text,
balance INTEGER )''')

number_card_list = list()

while True:
    print(
        """
        1. Create an account
        2. Log into account
        0. Exit
        """
    )

    user = input()

    if user == '0':
        print("Bye!")
        exit()

    if user == '1':
        card_user = BankCard()
        card_user.generate_card_number()
        cursor.execute(f"""INSERT INTO card (number, pin, balance ) VALUES ('{card_user.number_card}', '{card_user.pin_card}', '{card_user.balance}')""")

        conn.commit()
        number_card_list.append(card_user)

    if user == '2':
        print("Enter your card number:")
        number_card = input()
        print("Enter your PIN:")
        pin_card = input()
        card_user = BankCard()
        card_user.menu_account(number_card, pin_card)

conn.close()

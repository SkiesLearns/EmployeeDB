import mysql.connector
import re

class employee_database():

    def __init__(self, db):
        self.db = db
        self.mycursor = db.cursor()
        self.cursor = db.cursor(buffered=True)

    def display_db(self):
        self.mycursor.execute("SELECT * FROM employees")
        result = self.mycursor.fetchall()
        for row in result:
            print(f"""==========================================================
User ID = {row[0]}
==========================================================
Name = {row[1].title()}
Surname = {row[2].title()}
Age = {row[3]}
E-Mail = {row[4]}
Number = {row[5]}
Country = {row[6].title()}
City = {row[7].title()}""")

    def create_db(self):
        while True:
            name = input('Enter first name: ')
            if re.match("[A-Za-z]+$", name.lower()): break
            else: print('Incorrect input. Letters only.')

        while True:
            surname = input('Enter last name: ')
            if re.match("[A-Za-z]+$", surname.lower()): break
            else: print('Incorrect input. Letters only.')

        while True:
            country = input('Enter country: ')
            if re.match("[A-Za-z ]+$", country.lower()): break
            else: print('Incorrect input. Letters only.')

        while True:
            city = input('Enter city: ')
            if re.match("[A-Za-z ]+$", city.lower()): break
            else: print('Incorrect input. Letters only.')

        while True:
            try:
                age = int(input('Enter age: '))
                break
            except ValueError:
                print('Error in response. Numbers only.')

        while True:
            try:
                number = int(input('Enter phone number: '))
                break
            except ValueError:
                print('Error in response. Numbers only.')

        while True:
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            email = input('Enter e-mail address: ').lower()
            if re.fullmatch(regex, email): break
            else: print('E-Mail contained illegal characters, try again.')


        #Performs Query
        try:
            values = f"'{name}', '{surname}', '{age}', '{email}', '{number}', '{country}', '{city}'"
            query = f"INSERT INTO skies_company.employees (name, surname, age, email, number, country, city) VALUES ({values})"
            self.mycursor.execute(query)
            #Saves data to localhost
            self.db.commit()
            print('// ALL INFORMATION HAS BEEN STORED')
        except ValueError:
            print('Error while storing data. Try again.')

    def remove_db(self):
        email = input('Enter email linked to account: ').lower()

        try:
            query = "SELECT * FROM skies_company.employees WHERE email = %s;"
            self.cursor.execute(query, (email,))
            results = self.cursor.fetchall()
            for row in results:
                print(f"""==========================================================
Name: {row[1]}
Surname: {row[2]}
E-mail: {row[4]}
==========================================================""")
        except KeyError:
            print('Email not found.')

        while True:
            user_decide = input('Are you sure you want to delete? (Yes/No): ')
            if user_decide in ['yes', 'no']:
                try:
                    query = "DELETE FROM skies_company.employees WHERE email = %s;"
                    self.cursor.execute(query, (email,))
                    self.db.commit()
                    print('All information has been deleted.')
                    break
                except KeyError:
                    print('Error occurred while deleting data.')
            else:
                print(f"Invalid response, type 'yes' or 'no'.")

    def edit_db(self):
        #This makes sure the employee ID is in the database.
        while True:
            print('==========================================================')
            id = input('Enter your employee ID to manage your info: ')
            self.mycursor.execute('SELECT * FROM skies_company.employees WHERE id = %s', (id,))
            data = self.mycursor.fetchall()
            if data is None:
                print('No employee with provided ID.')
            else:
                break

        #Now that the ID is valid, we let the user change what they want.
        while True:
            user_decide = input("""To change info, type what you wish to change.
Name, Surname, Age, Email, Number, Country, City or Exit: """).lower()
            if user_decide not in ['name', 'surname', 'age', 'number', 'city', 'exit']:
                print('Invalid response, try again.')

            elif user_decide == 'exit': break

            else:
                new_value = input(f'Enter new {user_decide}: ')
                self.mycursor.execute(f"""UPDATE skies_company.employees SET {user_decide} = %s WHERE id = %s""",
                                     (new_value, id,))
                self.db.commit()
                print('Information successfully updated.')
                break


def main():
    db = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='Skies123',
            database='skies_company'
        )
    data = employee_database(db)

    while True:
        user_decide = input(f"""==========================================================
// EMPLOYEE DATABASE
To display current database type 'display'
To add new user information type 'create'
To edit existing information type 'edit'
To remove a user from database type 'remove'
To close application type 'quit'
: """).lower()
        if user_decide in ['display', 'create', 'remove', 'edit', 'quit']:
            if user_decide == 'quit':
                exit()
            else:
                action = getattr(data, f'{user_decide}_db')()
        else:
            print('Invalid input')

if __name__ == '__main__':
    main()

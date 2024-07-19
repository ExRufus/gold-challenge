import sqlite3
from employee import Employee

conn = sqlite3.connect('example.db')
c = conn.cursor()

# Memeriksa apakah tabel ada sebelum membuatnya
c.execute('''CREATE TABLE employees (
                    first text,
                    last test,
                    pay integer
                )''')

emp_1 = Employee('John', 'Doe', 8000)
emp_2 = Employee('Jane', 'Doe', 9000)

c.execute("INSERT INTO employees VALUES ('Mary', 'Schafer', 7000)")
# c.execute("INSERT INTO employees VALUES ('{}', '{}', {})".format(emp_1.first, emp_1.last, emp_1.pay))
# c.execute("INSERT INTO employees VALUES (?, ?, ?)", (emp_1.first, emp_1.last, emp_1.pay))

# conn.commit()

# c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", 
#           {'first': emp_2.first, 'last': emp_2.last, 'pay': emp_2.pay})

# conn.commit()

c.execute("SELECT * FROM employees WHERE last=?", ('Schafer',))
results = c.fetchall()

print(results)

# c.execute("SELECT * FROM employees WHERE last=:last", {'last': 'Doe'})
# print(c.fetchall())

# conn.commit()

conn.close()

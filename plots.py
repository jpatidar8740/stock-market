import matplotlib.pyplot as plt

import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

# Setting up database
mydb = mysql.connector.connect(
  host="localhost",
  user="jayant",
  passwd="Random"
)

c = mydb.cursor()
c.execute("USE test")


print('Enter SYMBOL of Stock?')
sym = input()

data = pd.read_sql("SELECT * FROM {}".format(sym), mydb)

plt.plot(range(len(data['Date'])), data['Curr'])
plt.show()

import matplotlib.pyplot as plt
import math
from datetime import datetime
import warnings

import requests
from bs4 import BeautifulSoup

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


# Read from csv and create tables.
data = pd.read_csv('companies.csv')
print(data)

for ind in data.index:
    name = data['SYMBOL'][ind]
    if name.find('_') == -1 and name.find('n') == -1:
        df = pd.read_sql("SELECT * from {}".format(name), mydb)
        if df.empty:
            print(name)
            data = data.drop(ind)

    else:
        print(name)
        data = data.drop(ind)

print(data)

data.to_csv('comp.csv', index=False)
mydb.commit()

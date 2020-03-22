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
"""mydb = mysql.connector.connect(
  host="localhost",
  user="jayant",
  passwd="Random"
)"""

engine = create_engine("mysql://jayant:Random@localhost/test")
con = engine.connect()

# Read from csv and create tables.
data = pd.read_csv('companies.csv')
names = data['SYMBOL']

print('UPTO.....')

c = False;

for name in names:
    print(name)

    if name.find('_') != -1 or name.find('n') != -1:
        continue

    if c:
        stmp = datetime.today()
        data = pd.read_csv("{}.csv".format(name))
        if data.empty:
            continue;
        #print(data)
        Open = data["Open"]
        High = data["High"]
        Low = data["Low"]
        Curr = data["Adj Close"]
        df = pd.DataFrame({
            'Date': [stmp]*(len(Open)),
            'Open': Open,
            'High': High,
            'Low': Low,
            'Curr': Curr
        });
        print(df)

        df.to_sql(con=con, name=name, if_exists='replace')

    if name == 'THIRUSUGAR':
        c = True

mydb.commit()

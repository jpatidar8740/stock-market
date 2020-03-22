import pandas as pd
import numpy as np
import statistics as st

from datetime import datetime
from datetime import timedelta
import time
import schedule

import mysql.connector

## Setting up database
mydb = mysql.connector.connect(
  host="localhost",
  user="jayant",
  passwd="Random"
)

c = mydb.cursor()
c.execute("USE test")

import utils

####BHAYANAK ASSUMPTION
## NO dividend payments and demand supply BAKAR, so day_end will be last close price, similarly for month and weeks
## No Volume involved in calc (Pata hai bahut hi galat hai, but mujhse abhi to itna hi hoga)

'''
This will update prices for all companies after every 5sec in trading time.
### What we have to do here?
#1 calculate mean and variance for all stocks till last date.(just once for today)
#2 use that m and v to predict prices for todays (Using GBM, *When you honestly do your finance lab assignments*)
#3 Save updated prices to database.

### #2 and #3 will be in loop after every 'x' sec.
# Exit at end of day.
'''


## TODO: Read File and store all Stock Symbols
companies = pd.read_csv('companies.csv')
global stock_sym

stock_sym = companies['SYMBOL']

data = []
## TODO:  for each stock cal mean and var of returns
def fetch_val():
    global data
    data = []
    stmp = datetime.now()
    print(stmp)
    # Don't run on Sat, Sun
    '''
    if(stmp.weekday() > 4):
        return'''

    for sym in stock_sym:
        print(sym)
        qry = ("SELECT * from {} WHERE Date < '{}'").format(sym, stmp)
        print(qry)
        frame = pd.read_sql(qry, mydb)
        #print(frame)
        ret = st.mean(utils.calc_return(frame["Curr"]))
        vr = st.stdev(utils.calc_return(frame["Curr"]))
        # just initializing vars like(High, Open, Low, Curr) will update them on first update
        data.append({'SYM': sym, 'mean': ret, 'var': vr, 'timestamp': datetime.now(), 'High': 0, 'Open': 0, 'Low': 0, 'Curr': 0})

    print(data)



# start first function (i.e. at just start of trading)
def start():
    global data
    print(data)
    new_data = []
    stmp = datetime.now()
    # Don't run on Sat, Sun
    """
    if(stmp.weekday() > 4):
        return"""

    for stk in data:
        frame = pd.read_sql(("SELECT * from {}").format(stk['SYM']), mydb)
        rw = utils.update_data_start(frame, stk['mean'], stk['var'])
        new_stk = {'timestamp': str(stmp), 'SYM': stk['SYM'], 'mean': stk['mean'], 'var': stk['var'], 'Open': rw[0], 'High': rw[1], 'Low': rw[2], 'Curr': rw[3]}
        new_data.append(new_stk)
        c.execute(("INSERT INTO {} VALUES ('{}', {}, {}, {}, {})").format(stk['SYM'], stmp, rw[0], rw[1], rw[2], rw[3]))

    mydb.commit()
    data = new_data

    print(stk)

    ## in loop (after every 10 sec) execute update function
    def update_loop():
        print('Update is running')
        new_data = []
        global data
        stmp = datetime.now()
        for stk in data:
            #frame = pd.read_sql(("SELECT * from {}").format(stk['SYM']), mydb)
            rw = utils.update_data(stk)
            print(rw)
            new_stk = {'timestamp': str(stmp), 'SYM': stk['SYM'], 'mean': stk['mean'], 'var': stk['var'], 'Open': rw[0], 'High': rw[1], 'Low': rw[2], 'Curr': rw[3]}
            new_data.append(new_stk)
            c.execute(("INSERT INTO {} VALUES ('{}', {}, {}, {}, {})").format(stk['SYM'], stmp, rw[0], rw[1], rw[2], rw[3]))

        mydb.commit()
        data = new_data

    schedule.every(5).seconds.do(update_loop).tag('real-time-update')
    update_loop()





## Times up, Close Trading, GO HOME.
## Before going home, save today's data in day wise tables of stock.'''
def save_day():
    global data
    stmp = datetime.today().date()
    print(stmp)
    for stk in data:
        # here curr is closing price for day
        c.execute(("INSERT INTO {} VALUES ('{}', {}, {}, {}, {})").format(stk['SYM'] + "_day", stmp, stk['Open'], stk['High'], stk['Low'], stk['Curr']))

    mydb.commit()

def save_week():
    global data
    stmp = datetime.today().date()
    print(stmp)
    for stk in data:
        # here curr is closing price for day
        c.execute(("INSERT INTO {} VALUES ('{}', {}, {}, {}, {})").format(stk['SYM'] + "_week", stmp, stk['Open'], stk['High'], stk['Low'], stk['Curr']))

    mydb.commit()

def save_month():
    # check whether it's last day of month or not?
    today_date = datetime.today()
    next_day = today_date + timedelta(1)
    # Next day date is less than it is last day of month
    if today_date.day > next_day.day:
        return

    global data
    stmp = datetime.today().date()
    print(stmp)
    for stk in data:
        # here curr is closing price for day
        c.execute(("INSERT INTO {} VALUES ('{}', {}, {}, {}, {})").format(stk['SYM'] + "_month", stmp, stk['Open'], stk['High'], stk['Low'], stk['Curr']))

    mydb.commit()

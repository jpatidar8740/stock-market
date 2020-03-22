import schedule

import trading
from datetime import datetime


t1 = input()
t2 = input()
t3 = input()
schedule.every().day.at("16:" + t1 + ":" + t2).do(trading.fetch_val)
schedule.every().day.at("16:"+ t1 + ":" + str(int(t2)+30)).do(trading.start)

# At the end of day save data in day wise
schedule.every().day.at("16:" + t3 + ":10").do(trading.save_day)

# At the end of each week, save data in week tables.
schedule.every().friday.at("16:" + t3 + ":40").do(trading.save_week)

# At the end of each month save data in month tables.
schedule.every().day.at("16:"+t3+":59").do(trading.save_month)

day_end = datetime.today().replace(hour=16, minute=int(t3), second=0, microsecond=0)
while True:
    schedule.run_pending()
    if datetime.today() > day_end:
        schedule.clear('real-time-update')

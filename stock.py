import pandas as pd
import os
import time
from datetime import datetime

path = "./intraQuarter"

def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    #print(stock_list)

    for each_dir in stock_list[1:]:
    # starting at 1 because it lists the root directory first
        each_file = os.listdir(each_dir)

        ticker = each_dir.split("/")[-1]
        # company abreviation 

        if len(each_file) > 0:
            # empty file
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())

                full_file_path = each_dir + "/" + file
                #print(full_file_path)
                source = open(full_file_path, "r").read()
                #print(source)
                value = source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split("</td>")[0]

                print(ticker + ": " + value)
            time.sleep(12)

Key_Stats()

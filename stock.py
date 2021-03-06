import pandas as pd
import os
import time
from datetime import datetime

path = "./intraQuarter"

def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]

    df = pd.DataFrame(columns=[
        "Date",
        "Unix",
        "Ticker",
        "DE Ratio",
        "Price", # would drop if space were a concern, big data set
        "stock_p_change",
        "S&P500", # would also drop...
        "sp500_p_change"])
    #data frame

    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")

    ticker_list = []

    for each_dir in stock_list[1:25]:
    # starting at 1 because it lists the root directory first
        each_file = os.listdir(each_dir)

        ticker = each_dir.split("/")[-1]
        # company abreviation 
        ticker_list.append(ticker)

        starting_stock_value = False
        starting_sp500_value = False

        if len(each_file) > 0:
            # empty file
            for file in each_file:
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())

                full_file_path = each_dir + "/" + file
                source = open(full_file_path, "r").read()
                try:
                    value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split("</td>")[0])

                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adj Close"])
                    except Exception as e:
                        sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
                        # 259200 = 3 days in seconds, gets us out of the weekend
                        # or holiday. Simple approximation to fudge an estimate
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adj Close"])

                    stock_price = float(source.split('</small><big><b>')[1].split("</b></big>")[0])
                    # print("stock_price: ", stock_price, "ticker: ", ticker)

                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value

                    stock_p_change = 100 * ((stock_price - starting_stock_value)/starting_stock_value)
                    sp500_p_change = 100 * ((sp500_value - starting_sp500_value)/starting_sp500_value)
                    # stock percent change. Stock_price = new price,


                    df = df.append({
                        "Date": date_stamp,
                        "Unix": unix_time,
                        "Ticker": ticker,
                        "DE Ratio": value,
                        "Price":  stock_price,
                        "stock_p_change": stock_p_change,
                        "S&P500": sp500_value,
                        "sp500_p_change": sp500_p_change}, ignore_index=True)
                except Exception as e:
                    # could be catching values that wont be a float or no value
                    pass

    save = gather.replace(" ","").replace("(","").replace(")","").replace("/","") + str(".csv")
    print(save)
    df.to_csv(save)
    time.sleep(10)

Key_Stats()

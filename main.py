import pandas as pd
from bs4 import BeautifulSoup
from selenium  import webdriver
import csv
import time

def replace_prices(text):
    return text.replace("٬","").replace("۰","0").replace("۱","1").replace("۲","2").replace("۳","3").replace("۴","4").replace("۵","5").replace("۶","6").replace("۷","7").replace("۸","8").replace("۹","9")

def replace_percentages(text):
    return text.replace("٪","").replace("٫",".").replace("٬",".").replace("۰","0").replace("۱","1").replace("۲","2").replace("۳","3").replace("۴","4").replace("۵","5").replace("۶","6").replace("۷","7").replace("۸","8").replace("۹","9")

def scrapping(file):
    driver = webdriver.Chrome()
    # driver = webdriver.Firefox()
    name_list = []
    close_list = []
    percentage_list = []
    cash_list = []
    overall_cash = int(file['Remained'][0])
    for i in range(len(file['Website'])):
        driver.get(file['Website'][i])
        soup = BeautifulSoup(driver.page_source,"lxml")
        name = soup.select('.asset-symbol')[0].text.strip()
        name_list.append(name)
        close_percentage = replace_percentages(soup.select('.pos')[3].text)
        percentage_list.append(close_percentage)
        close_price = replace_prices(soup.select('.symbolprices')[0].select("span")[0].text)
        close_list.append(f"{int(close_price):,d}")
        number = file['Number'][i]
        cash_without_tax = number * int(close_price)
        print(cash_without_tax)
        cash = int(cash_without_tax - (0.015 * cash_without_tax))
        cash_list.append(f"{cash:,d}")
        overall_cash = overall_cash + cash
        print("Name: "+ name)
        print("Number: "+ str(number))
        print("Close Price: "+ f"{int(close_price):,d}")
        print("Close Price Percentage: "+ close_percentage)
        print("Stock: "+ str(f"{cash:,d}"))
        print("\n")
    overall_cash = f"{overall_cash:,d}"
    print("Overall Stock: "+ str(overall_cash))
    driver.quit() 
    return name_list, close_list, percentage_list, cash_list, overall_cash

def writing(file, names, close, percentage, cash, overall_cash):
    with open('stock.csv', mode='w', newline='\n') as csv_file:
            st = csv.writer(csv_file, delimiter=',')
            st.writerow(['Stock', 'Number', 'Close', 'Percentage', 'Cash', 'Remained', 'Overall_Cash', 'Website'])
            st.writerow([names[0], file['Number'][0], close[0], percentage[0], cash[0], file['Remained'][0], overall_cash, file['Website'][0]])
            for i in range(1, len(file)):
                st.writerow([names[i], file['Number'][i], close[i], percentage[i], cash[i], '', '', file['Website'][i]])

def make_file():
    with open('stock.csv', mode='w', newline='\n') as csv_file:
        st = csv.writer(csv_file, delimiter=',')
        st.writerow(['Stock', 'Number', 'Close', 'Percentage', 'Cash', 'Remained', 'Overall_Cash', 'Website'])
        websites = ['https://rahavard365.com/asset/7792/غگیلا', 'https://rahavard365.com/asset/327/پیزد', 'https://rahavard365.com/asset/7804/آریا', 'https://rahavard365.com/asset/350/خاذین', 'https://rahavard365.com/asset/2049/وپویا']
        numbers = [14, 14, 57, 5950, 228]
        st.writerow(['',numbers[0],'','','',69214,'',websites[0]])
        for i in range(1, len(websites)):
            st.writerow(['',numbers[i],'','','','','',websites[i]])

def main():
    make_file()
    file = pd.read_csv('stock.csv')
    names, close_list, percentage_list, cash_list, overall_cash = scrapping(file)
    writing(file, names, close_list, percentage_list, cash_list, overall_cash)

main()

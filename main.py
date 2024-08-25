from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import os
import csv
import re
from datetime import datetime


def make_file_name():
    now = datetime.now()
    return now.strftime("%d-%m-%Y") + '-wnba.csv'


def remove_csvs_older_than_n_days(n=7):
    now = datetime.now()
    for file in os.listdir():
        if file.endswith('.csv'):
            date = file.replace('-wnba.csv', '')
            date = datetime.strptime(date, "%d-%m-%Y")
            if (now - date).days > n:
                os.remove(file)


def make_row(rank, tds):
    row = []
    col = 0
    row.append(rank)
    in_playoffs = False
    for table_data in tds:
        text = table_data.text
        text = re.sub(r'\s+', '', text)
        if col == 0:
            text = re.sub(r'\d+', '', text)
            if 'Close' in text:
                text = text.replace('Close', '')
                in_playoffs = True
        row.append(text)
        col += 1
    row.append(in_playoffs)
    return row


def main():
    url = 'https://www.wnba.com/standings'
    html = urlopen(url).read().decode("utf-8")
    soup = bs(html, "html.parser")
    table_rows = soup.find('table').find_all('tr')
    table_headers = soup.find('table').find_all('th')

    filename = make_file_name()
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)

        headers = ["RANK"]
        for th in table_headers:
            headers.append(th.text)
        headers.append("PLAYOFFS")
        writer.writerow(headers)

        rank = 1
        for table_row in table_rows:
            table_data = table_row.find_all('td')
            if len(table_data) == 0:
                continue
            row = make_row(rank, table_data)
            writer.writerow(row)
            rank += 1
    remove_csvs_older_than_n_days(7)


if __name__ == '__main__':
    main()

from html.parser import HTMLParser
from time import sleep
import urllib.request as urllibReq
import re
import csv

def clean_html(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

URL = 'https://btce.penek.org/chat_history/ru/'
NAME = 'chat_log'
_END = '.html'

year = 2011     #start year is 2011
month = 7       #start month is 7
day = 8         #real start day is 12
                #this is the date of the first message appeared on the chat
end_year = 2017 #end date
end_month = 7
end_day = 18

while True:
    day += 1
    
    #end date
    if year == end_year and month == end_month and day == end_day:
        break
    
    if day > 31:
        day = 1
        month += 1
    
    if month > 12:
        month = 1
        year += 1
    
    #if day or month less than 10 add '0' before it
    #this is for correct url address
    
    str_day = ('0' if (day < 10) else '') + str(day) 
    str_month = ('0' if (month < 10) else '') + str(month)
    str_year = str(year)

    name = 'chat_log_' + str_year[2:] + '-' + str_month + '-' + str_day + '.csv'

    print(name)
    
    url = URL + str_year + '/' + str_month + '/' + str_day + _END
    req = urllibReq.Request(url)

    
    try:
        resp = urllibReq.urlopen(req)
        
    except:
        continue

    else:
        c = resp.read().decode('utf-8')
        
    
    messages = re.split('<br />\n', c)
    norm_time = []
    epochs_time = []
    nickname = []
    msg_text = []

    messages.pop()

    with open(name, 'w', newline = '') as csvfile:
        fieldnames = ['normal_date', 'epochs', 'nickname', 'message_text']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()

        for message in messages:
            norm_time = re.search(r'\d{2}:\d{2}:\d{2}', message).group(0).encode('utf-8')
            epochs_time = re.search(r'\d{10}', message).group(0).encode('utf-8')
            nickname = re.search(r'.{74}(\b\w+)', message).group(0)[74:].encode('utf-8')
            msg_text = message[(message.find('</span>: ') + 9):]

            if len(msg_text) >= 1 and msg_text[0] != '"':
                msg_text = '"' + msg_text

            if len(msg_text) >= 1 and msg_text[-1] != '"':
                msg_text += '"'

            try:
                writer.writerow({'normal_date':norm_time.decode('utf-8'), 'epochs':epochs_time.decode('utf-8'),
                             'nickname':nickname.decode('utf-8'), 'message_text':clean_html(msg_text).encode('utf-8').decode('utf-8')})

            except:
                continue

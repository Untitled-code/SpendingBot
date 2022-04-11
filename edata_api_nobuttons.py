#!/usr/bin/python3
# e-data API get
import requests
import time
import datetime
import logging, json
from pathlib import Path
import csv

logging.basicConfig(filename='spending_bot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.debug('Start of program')

def emit_row(output_file, row): #get data to csv
    if output_file.is_file():
        with open(output_file, 'a') as o_file:
            fieldnames = row.keys()
            writer = csv.DictWriter(o_file, fieldnames=fieldnames)
            writer.writerow(row)
    else:
        with open(output_file, 'w') as o_file:
            fieldnames = row.keys()
            writer = csv.DictWriter(o_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(row)

def request(sender, reciever, starDate, endDate, output_file):
    global totalAmount
    totalAmount = []
    print(sender, reciever, starDate, endDate, output_file)
    OUTPUT_FILE = Path(output_file)
    """Adding parameters of the search depending on what keyword we need to search"""
    PAYER = f'payers_edrpous={sender}'
    RECIPT = f'recipt_edrpous={reciever}'
    REGION = ''
    """end"""
    rangePairDates = getDates(starDate, endDate)
    for m in range(len(rangePairDates)):
        relation = {} # forming dictitory to record key(fields name) and values from e data
        STARTDATE = f'startdate={rangePairDates[m][0]}' #get start date for which period we look
        ENDDATE = f'enddate={rangePairDates[m][1]}'
        try:
            time.sleep(2)
            response = requests.get(f'http://api.spending.gov.ua/api/v2/api/transactions/?{PAYER}&{RECIPT}&{REGION}&{STARTDATE}&{ENDDATE}')
            response.raise_for_status()
            # Load JSON data info
            resultDict = json.loads(response.text)
            for i in range(len(resultDict)):
                # time.sleep(0.5)
                print(f'Entity:{sender} {reciever}, OUTER LOOP:{str(m)}, INNER:{str(i)}')
                if resultDict: #check if resultDict has values
                    # print(resultDict[i]['payer_name'])
                    # print(resultDict[i]['payer_edrpou'])
                    # print(str(int(resultDict[i]['amount'])/1000) + ' тыс')
                    # print(resultDict[i]['recipt_name'])
                    # print(resultDict[i]['recipt_edrpou'])
                    # print(resultDict[i]['trans_date'])
                    # print(resultDict[i]['payment_details'])
                    # print('______________')
                    totalAmount.append(int(resultDict[i]['amount']))
                    """getting all data - making field names and values"""
                    relation['payers_name'] = (resultDict[i]['payer_name'])
                    # relation['payers_name'] = ', '.join(resultDict[i]['payer_name'])
                    relation['payer_edrpou'] = (resultDict[i]['payer_edrpou'])
                    relation['amount'] = (resultDict[i]['amount'])
                    relation['recipt_name'] = (resultDict[i]['recipt_name'])
                    relation['recipt_edrpou'] = (resultDict[i]['recipt_edrpou'])
                    relation['trans_date'] = (resultDict[i]['trans_date'])
                    relation['payment_details'] = (resultDict[i]['payment_details'])
                    # print(relation)
                    emit_row(OUTPUT_FILE, relation) #putting all in csv

        except requests.exceptions.ConnectionError as e:
            print("Error Connecting:", e)
           # keywords.pop(keyword)
           # print(f"Key words left {keywords}")
            print("Sleep fo 30 min")
            time.sleep(60*30)
    return totalAmount

def getDates(start, end):
    rangeDates = []
    countDays = end - start
    print(countDays)
    countDays = countDays.days  # getting how many times we need to loop
    print(countDays)
    for i in range(0, int(countDays+1), 31): #loop for every 91 day
        newDate = start + datetime.timedelta(days=i) #getting date in a range
        dateString1 = newDate.strftime('%Y-%m-%d') #converting into string for the type
        print(newDate)
        rangeDates.append(dateString1)
    rangePairDates = [[rangeDates[i], rangeDates[i+1]] for i in range(len(rangeDates)-1)]
    print(rangePairDates)
    return rangePairDates
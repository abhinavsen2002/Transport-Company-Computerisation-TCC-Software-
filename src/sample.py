'''
import bill

consignSample = {
    '_id': id, 
    'Volume': 100,
    'Sender Name': 'Yash', 
    'Sender Address': '21, RK Nagar, Bangalore',
    'Sender Phone': "9853224324", 
    'Sender Mail': 'ytharthsmr@gmail.com',
    'Receiver Name': 'Jay', 
    'Receiver Address': "9, Bank Colony, Ratlam", 
    'Receiver Phone': '8623879463',
    'Date Of Arrival': '20-03-12',
    'Date Of Dispatch': '23-03-12',
    'Cost': 10000
    }

bill.bill(consignSample)
'''

from datetime import datetime, date
s1 = datetime.strptime('2022-05-01', '%Y-%m-%d')
s2 = datetime.strptime('2022-05-01 05:00:00', '%Y-%m-%d %H:%M:%S')
print(s1 < s2)
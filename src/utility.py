import pymongo
import random
from employee import changePassword
import consign
import string
from datetime import date
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent='TCC')

def distance(city1, city2):
    location1 = geolocator.geocode(city1)
    location2 = geolocator.geocode(city2)
    return geodesic((location1.latitude, location1.longitude), (location2.latitude, location2.longitude)).km

def closestBranch(address):
    city = address.split(', ')[-1]
    minDistance = 100000
    closestBranch = ''
    for branch in branchDB.find():
        if distance(city, branch['Location']) < minDistance:
            minDistance = distance(city, branch['Location'])
            closestBranch = branch['Location']
    return closestBranch


class Branch:
    def __init__(self, location, address, employees = [], numOfEmployees = 0, revenue = 0) -> None:
        self.location = location
        self.address = address
        self.employees = employees
        self.numOfEmployees = numOfEmployees
        self.revenue = revenue
        
    def convertToDictAndUpload(self) -> None:
        global settings
        id = settings.find_one({'_id':0})['BranchID']
        settings.update_one({'_id':0}, {'$set':{'BranchID':id+1}})
        branchDB.insert_one({
            '_id': id, 
            'Location':self.location, 
            'Address':self.address, 
            'Number Of Employees': self.numOfEmployees, 
            'Employees': self.employees, 
            'Revenue': self.revenue})

    def convertFromDict(dict):
        return Branch(dict['Location'], dict['Address'], dict['Employees'], dict['Number Of Employees'], dict['Revenue'])


def checkLogin(username, password):
    try:
        if username == "admin" and password == settings.find_one({'_id': 0})['managerPassword']:
            return 'SU'
        elif username == employeeDB.find_one({'email': username})['email'] and password == employeeDB.find_one({'email': username})['password']:
            return True
    except:
        return False

def generateRandomString():
    return ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randint(8, 12)))

def today():
    return str(date.today())

def setupDB():
    global database, employeeDB, settings, branchDB, truckDB, consignDB
    cluster = pymongo.MongoClient("mongodb+srv://selabproject:selabproject@se.hl6lf.mongodb.net/TCC?retryWrites=true&w=majority")
    database = cluster['TCC']
    settings = database['Settings']
    employeeDB = database['Employee']
    branchDB = database['Branch']
    consignDB = database['Consignment']
    truckDB = database['Truck']

def mailPassword(email):
    try:
        # mail password
        password = generateRandomString()
        changePassword(email, password)
        return True
    except:
        return False

def nextEmptyTruckID(branch):
    truck =truckDB.find_one({'Branch': branch, 'Next Destination': 'NA'}) 
    if truck is not None:
        return truck['_id']
    return None

def loadUnloadedConsignments(branch):
    consignments = consignDB.find({'At Branch': branch, 'Status': 'Unloaded'})
    curTruckID = nextEmptyTruckID(branch)
    for consignment in consignments:
        if curTruckID is None:
            return
        if consign.loadConsignment(consignment['_id'], curTruckID):
            curTruckID = nextEmptyTruckID(branch)

database = None
settings = None
employeeDB = None
branchDB = None
consignDB = None
truckDB = None

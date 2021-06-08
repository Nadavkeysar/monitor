import win32con
import win32service
from threading import Timer
from datetime import datetime
from dateutil import parser
from pandas.tests.extension import test_string

prev_services = []

#Function to find difference of 2 lists
def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))
    
def Monitor():
    current_services = []
    myfile = open('serviceList.txt', 'a')
    myfile.write("Date ")
    date_string = str(datetime.date(datetime.now()))
    myfile.write(date_string+"  ")

    resume = 0
    accessSCM = win32con.GENERIC_READ
    accessSrv = win32service.SC_MANAGER_ALL_ACCESS

    #Open Service Control Manager
    hscm = win32service.OpenSCManager(None, None, accessSCM)

    #Enumerate Service Control Manager DB
    typeFilter = win32service.SERVICE_WIN32
    stateFilter = win32service.SERVICE_STATE_ALL

    statuses = win32service.EnumServicesStatus(hscm, typeFilter, stateFilter)

    for (short_name, desc, status) in statuses:
        print(short_name, desc, status) 

    print("\n")
    for (short_name, desc, status) in statuses:
        
        myfile.write(short_name)
        current_services.append(short_name) 
    
    	
    myfile.write("\n\n")
    myfile.close()
    
    #For Status_log.txt
    closed_services = Diff(prev_services,current_services)
    extra_services = Diff(current_services,prev_services)

    ##Writing closed services in Status_log.txt
    status = open("Status_log.txt", "w")
    status.write("Closed Services are as follows : \n")
    for element in closed_services:
        status.write(element + "\n")

    ##Writing newly added services in Status_log.txt        
    status.write("New Added Services are as follows : \n")    
    for element in extra_services:
        status.write(element + "\n")

    myfile.close()

def Manual():
    print("Enter starting date 1 : ")
    date1 = parser.parse(input("Enter date1 DD-MM-YYYY : "))
    date11 = str(date1)
    
    print("Enter end date  ")
    date2 = parser.parse(input("Enter end date2 DD-MM-YYYY : "))
    date22 = str(date2)
    
    myfile = open('serviceList.txt', 'r')
    # read file content
    readfile = myfile.read()
    if date11 in readfile:
	    pass
    else:
        print('Date', date1, ' Not Found In File')
        return
    if date22 in readfile:
	    pass
    else:
        print('Date', date2, ' Not Found In File')
        return
    service_date1 = []
    service_date2 = []
    do = False
    do1 = False
    res = test_string.split() 
    # printing result 
    for i in res:
        if(i == date11):
            do = True
        if(do):
            service_date1.append(i)
        if(do1):
            service_date2.append(i)
        if(i== "Date"):
            do = False
            do1 = False
        if(i== date22):
            do1 = True
    service_date1 = list(sorted(service_date1 - service_date2))
    service_date2 = list(sorted(service_date2 - service_date1))
    
    print("Services closed : ", service_date1)
    print("Services opened : ", service_date2)

def Display():
    print("\nBelow are the modes available:\n\n1.Monitor Mode \n2.Manual Mode \n3.Exit")
def choice(a):
    if(a == 1):
        Monitor()
    elif(a==2):
        Manual()
    else:
        exit();
ch = 0
while ch != 4:
    Display()
    ch = int(input("ENTER YOUR CHOICE = "))
    choice(ch)
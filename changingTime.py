


from datetime import datetime, date, timedelta
import sys
import time
#import datetime, calendar
#import datetime

#print(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
#print(datetime.today().strftime('%Y-%m-%d'))

#startDate = '2019-02-13'

giveDate = sys.argv[1]
interval = sys.argv[2]
sleepTime = sys.argv[3]

giveDate = giveDate.split("-")

startDate = date(int(giveDate[0]),int(giveDate[1]),int(giveDate[2]))

endYear = datetime.today().strftime('%Y')
endMonth = datetime.today().strftime('%m')
endDay = datetime.today().strftime('%d')
endDate = date(int(endYear),int(endMonth),int(endDay))

delta = endDate - startDate

before = ''
after = ''

nowDay = datetime.today().strftime('%Y-%m-%d')
nowHour = datetime.today().strftime('%H:%M:%S')
now = nowDay+'T'+nowHour+'Z'
print(now)

c = 0
while 1:
    print("\n getting data ... ")
    #print(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))

    

    for d in range(delta.days + 2):
        day = startDate + timedelta(days = d)
        if(d>(1-int(interval))):
            dayBefore = startDate + timedelta(days = d-int(interval))
        c+=1
        #print(d) #d = 0,1,2...
        if (c<int(interval)):
            continue
        elif (c==int(interval)):
            day = str(day) 
            newdate = day.split("-")
            newdate = str(newdate[0])+'-'+str(newdate[1])+'-'+str(newdate[2])+'T00:00:00Z'

            if(d>0):
                dayBefore = str(dayBefore) 
                dateBefore = dayBefore.split("-")
                dateBefore = str(dateBefore[0])+'-'+str(dateBefore[1])+'-'+str(dateBefore[2])+'T00:00:00Z'

                before = dateBefore
                after = newdate

                beginDate = before
                endDate = after

                #print("=================================================================================")
                print("\n ================== FROM: ",beginDate)
                print(" ================== TO: ",endDate+"\n")
                #print("=================================================================================")


            c = 0

    nowDay = datetime.today().strftime('%Y-%m-%d')
    nowHour = datetime.today().strftime('%H:%M:%S')
    now = nowDay+'T'+nowHour+'Z'
    print(now)
    
    time.sleep(int(sleepTime))
    


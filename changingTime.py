


from datetime import datetime, date, timedelta
import sys
#import time
#import datetime, calendar
#import datetime

#print(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
#print(datetime.today().strftime('%Y-%m-%d'))

#startDate = '2019-02-13'

giveDate = sys.argv[1]
interval = sys.argv[2]
giveDate = giveDate.split("-")

startDate = date(int(giveDate[0]),int(giveDate[1]),int(giveDate[2]))

endYear = datetime.today().strftime('%Y')
endMonth = datetime.today().strftime('%m')
endDay = datetime.today().strftime('%d')
#print(endYear,endMonth,endDay)
endDate = date(int(endYear),int(endMonth),int(endDay))

delta = endDate - startDate


#before = str(giveDate[0])+'-'+str(giveDate[1])+'-'+str(giveDate[2])+'T00:00:00Z'
before = ''
after = ''

c = 0
for d in range(delta.days + 2):
    
    day = startDate + timedelta(days = d)
    if(d>0):
        dayBefore = startDate + timedelta(days = d-1)
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

            print("\nBefore -> ", before)
            print("After  -> ", after)
        c = 0


"""
# mes a mes
newyear20=0

before = '2009-08-01T00:00:00Z'
after = '2010-01-01T00:00:00Z'

for ano in range (-1,12): #(-1,12)
    for mes in range(1,13): #todos os meses ... 11 anos * 12 meses = 132 meses
        print(" . . . NOVO INTERVALO DE TEMPO")
        #time.sleep(60*4) #86400 = 1 dia sleep, 3600s = 1h
        #print(ano,mes)
        if(ano<10):
            if (ano == -1 and mes >= 8):
                if (mes < 10):
                    before = '2009-0'+str(mes)+'-01T00:00:00Z'
                    if((mes+1) == 10):
                        after = '2009-'+str((mes+1))+'-01T00:00:00Z'
                    else:
                        after = '2009-0'+str(mes+1)+'-01T00:00:00Z'
                else:
                    before = '2009-'+str(mes)+'-01T00:00:00Z'
                    if(mes < 12):
                        after = '2009-'+str(mes+1)+'-01T00:00:00Z'
                    else:
                        after = '2010-01-01T00:00:00Z'
            elif (ano == -1 and mes < 8):
                continue
            elif(ano > -1):
                if (mes < 10):
                    before = '201'+str(ano)+'-0'+str(mes)+'-01T00:00:00Z'
                    if((mes+1) == 10):
                        after = '201'+str(ano)+'-'+str((mes+1))+'-01T00:00:00Z'
                    else:
                        after = '201'+str(ano)+'-0'+str(mes+1)+'-01T00:00:00Z'
                else:
                    before = '201'+str(ano)+'-'+str(mes)+'-01T00:00:00Z'
                    if(mes < 12):
                        after = '201'+str(ano)+'-'+str(mes+1)+'-01T00:00:00Z'
                    else:
                        if(ano<9):
                            after = '201'+str(ano+1)+'-01-01T00:00:00Z'
                        else:
                            after = '20'+str(10+ano+1)+'-01-01T00:00:00Z'
        elif(ano>=10):
            #datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            #print(datetime.today().strftime('%Y-%m-%d'))
            #print(datetime.today().strftime('%Y-%m-%d'))
            mesAtual = datetime.today().strftime('%m')
            anoAtual = datetime.today().strftime('%Y')
            
            if(int(mesAtual) < 10):
                mesAtual = mesAtual[1]

            #print(mesAtual, mes)
            year = 2000+ano+10
            #print(anoAtual,year)
                        
            if (mes < 10):
                before = '20'+str(ano+10)+'-0'+str(mes)+'-01T00:00:00Z'
                if((mes+1) == 10):
                    after = '20'+str(ano+10)+'-'+str((mes+1))+'-01T00:00:00Z'
                else:
                    after = '20'+str(ano+10)+'-0'+str(mes+1)+'-01T00:00:00Z'
            else:
                before = '20'+str(ano+10)+'-'+str(mes)+'-01T00:00:00Z'
                if(mes < 12):
                    after = '20'+str(ano+10)+'-'+str(mes+1)+'-01T00:00:00Z'
                else:
                    if(ano<9):
                        after = '20'+str(ano+1+10)+'-01-01T00:00:00Z'
                    else:
                        after = '20'+str(ano+1+10)+'-01-01T00:00:00Z'

            if(int(anoAtual)==year):
                if(int(mesAtual) < mes):
                    break
        else:
            continue

        print(before)
        print(after)

        #time.sleep(5)
"""
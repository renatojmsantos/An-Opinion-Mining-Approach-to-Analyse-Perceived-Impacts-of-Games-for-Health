from datetime import datetime
import time

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

        time.sleep(5)

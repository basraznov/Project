import PredicTrade as pt
import datetime
import sys

symbol = str(sys.argv[1])
fdate = str(sys.argv[2])
ldate = str(sys.argv[3])
money = int(sys.argv[4])
# = datetime.strptime(fdate, '%Y-%m-%d')
fdate = datetime.datetime.strptime(fdate, "%Y-%m-%d").date()
ldate = datetime.datetime.strptime(ldate, "%Y-%m-%d").date()
# print(fdate,ldate)
p = pt.predic(symbol)
# datetime yyyy mm dd
# fdate = datetime.date(2018, 1, 1)
# ldate = datetime.date(2018, 4, 1)
now = datetime.datetime.now().date()

ft = 0
lt = 0
if fdate != now and ldate <= now and ldate > fdate:
    for x in range(len(p)):
        if p[x][0] ==  fdate:
            ft += 1
        if ft == 0 and p[x][0] > fdate:
            fdate = p[x][0]
            ft += 1
            
        if p[x][0] ==  ldate:
            lt += 1
        if lt == 0 and p[x][0] > ldate:
            ldate = p[x][0]
            lt += 1
    fl = [x for x in p if fdate in x][0]
    t = 0
    for x in p:
        if ldate in x:
            t += 1
    if t == 0:
        ldate = p[-1][0]
    ll = [x for x in p if ldate in x][0]
    fn = p.index(fl)
    ln = p.index(ll)
    interes = []
    for x in range(fn,ln):
        interes.append(p[x])

    buyrate = 1.001570
    sellrate = 0.998430
    stock = 0
    m = 0
    n = 0
    k = 0
    selltime = 3
    price = 0
    oldstock = 0
    tstock = 0

    for x in range(len(interes)):
        # print(interes[x])
        price = interes[x][1]
        if interes[x][2] == 'Buy ' and money != 0:
            money = money / buyrate
            stock += money / price
            # oldstock = stock
            money = 0
            m += 1
            #Date Trend Price Dealing_Stock Remain_Stock Remain_Money
            print('["',interes[x][0],'","buy","',price,'","',stock,'","',stock,'","',money,'"]')
            k = 0 
        if interes[x][2] == 'Sell' and stock != 0:
            if selltime == 2:
                if k == 0:
                    tstock = stock
                    money += price*stock*(0.5)
                    money = money * sellrate
                    print('["',interes[x][0],'","sell","',price,'","',tstock*(0.5),'","',stock,'","',money,'"]')
                    stock = stock * 0.5
                    k += 1
                else:
                    tstock = stock
                    money += price*stock
                    money = money * sellrat
                    print('["',interes[x][0],'","sell","',price,'","',tstock,'","',stock,'","',money,'"]')
                    stock = 0
                    k = 0
                n += 1
            if selltime == 3:
                if k == 0:
                    tstock = stock
                    money += price*stock*(0.33)
                    stock -= stock * 0.33
                    money = money * sellrate
                    print('["',interes[x][0],'","sell","',price,'","',tstock*(0.33),'","',stock,'","',money,'"]')
                    # print('["Date":"',interes[x][0],'","Trend":"sell","Price":"',price,'","Dealing_Stock":',tstock*(0.33),'","Remain Stock',stock,'","Remain Money',money,'],')
                    k += 1
                elif k == 1:
                    tstock = stock
                    money += price*stock*(0.5)
                    stock -= stock * 0.5
                    money = money * sellrate
                    print('["',interes[x][0],'","sell","',price,'","',tstock*(0.5),'","',stock,'","',money,'"]')
                    # print('["Date":"',interes[x][0],'","Trend":"sell","Price":"',price,'","Dealing_Stock":',tstock*(0.5),'","Remain Stock',stock,'","Remain Money',money,'],')
                    k += 1
                else:
                    tstock = stock
                    money += price*stock
                    stock = 0
                    money = money * sellrate
                    print('["',interes[x][0],'","sell","',price,'","',tstock,'","',stock,'","',money,'"]')
                    # print('["Date":"',interes[x][0],'","Trend":"sell","Price":"',price,'","Dealing_Stock":',tstock,'","Remain Stock',stock,'","Remain Money',money,'],')
                    k = 0
    tstock = 0
    if stock == 0:
        #stock worth money
        # print("You don't have stock. You have money",money)
        print('["0","0","',money,'"]')
    elif stock != 0 and money != 0:
        # print("You have",stock,"stock Worth ",stock*price,"and Money",money,"  ",stock*price+money)
        print('["',stock,'","',stock*price,'","',money,'"]')
    else:
        # print("You have",stock,"stock Worth ",stock*price)
        print('["',stock,'","',stock*price,'","',money,'"]')
else:
    print("wrong date")
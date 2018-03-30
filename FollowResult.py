import PredicTrade as pt
import datetime

p = pt.predic("KBANK")

# datetime yyyy mm dd
fdate = datetime.date(2018, 1, 1)
ldate = datetime.date(2018, 3, 28)
now = datetime.datetime.now().date()

ft = 0
lt = 0
if fdate != now and ldate <= now:
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
    money = 100000
    stock = 0
    m = 0
    n = 0
    k = 0
    selltime = 3
    price = 0
    oldstock = 0
    tstock = 0

    for x in range(len(interes)):
        print(interes[x])
        price = interes[x][1]
        if interes[x][2] == 'Buy ' and money != 0:
            money = money / buyrate
            stock += money / price
            # oldstock = stock
            money = 0
            m += 1
            # print("------------------------------------------------\nStock =",stock,"|Money =",money,"|Price buy =",price,"\n------------------------------------------------")
            print("----------------------------------------------------------------------\nBuy at",price,"| Buy",stock,"Stock | Remain Stock",stock,"| Remain Money",money,"\n----------------------------------------------------------------------")
            k = 0 
        if interes[x][2] == 'Sell' and stock != 0:
            if selltime == 2:
                if k == 0:
                    tstock = stock
                    money += price*stock*(0.5)
                    money = money * sellrate
                    print("----------------------------------------------------------------------\nSell at",price,"| Sell",tstock*(0.5),"Stock | Remain Stock",stock,"| Remain Money",money,"\n----------------------------------------------------------------------")
                    stock = stock * 0.5
                    k += 1
                else:
                    tstock = stock
                    money += price*stock
                    money = money * sellrat
                    print("----------------------------------------------------------------------\nSell at",price,"| Sell",tstock,"Stock | Remain Stock",stock,"| Remain Money",money,"\n----------------------------------------------------------------------")
                    stock = 0
                    k = 0
                n += 1
            if selltime == 3:
                if k == 0:
                    tstock = stock
                    money += price*stock*(0.33)
                    stock -= stock * 0.33
                    money = money * sellrate
                    print("----------------------------------------------------------------------\nSell at",price,"| Sell",tstock*(0.33),"Stock | Remain Stock",stock,"| Remain Money",money,"\n----------------------------------------------------------------------")
                    k += 1
                elif k == 1:
                    tstock = stock
                    money += price*stock*(0.5)
                    stock -= stock * 0.5
                    money = money * sellrate
                    print("----------------------------------------------------------------------\nSell at",price,"| Sell",tstock*(0.5),"Stock | Remain Stock",stock,"| Remain Money",money,"\n----------------------------------------------------------------------")
                    k += 1
                else:
                    tstock = stock
                    money += price*stock
                    stock = 0
                    money = money * sellrate
                    print("----------------------------------------------------------------------\nSell at",price,"| Sell",tstock,"Stock | Remain Stock",stock,"| Remain Money",money,"\n----------------------------------------------------------------------")
                    k = 0
    tstock = 0
    if stock == 0:
        print("You don't have stock. You have money",money)
    elif stock != 0 and money != 0:
        print("You have",stock,"stock Worth ",stock*price,"and Money",money,"  ",stock*price+money)
    else:
        print("You have",stock,"stock Worth ",stock*price)
else:
    print("wrong date")
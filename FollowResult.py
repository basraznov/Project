import PredicTrade as pt
import datetime

p = pt.predic("AFC")

# datetime yyyy mm dd
fdate = datetime.date(2018, 1, 1)
ldate = datetime.date(2018, 3, 21)
now = datetime.datetime.now().date()

# print(now,fdate,now > fdate,now < fdate)

# if p[0][0] < fdate:
#     print("First can't before",p[0][0])
#     exit()
# if fdate > now:
#     fdate = now
# if ldate > now:
#     ldate = now
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
    print(ldate)
    fl = [x for x in p if fdate in x][0]
    ll = [x for x in p if ldate in x][0]
    fn = p.index(fl)
    ln = p.index(ll)
    interes = []
    for x in range(fn,ln):
        interes.append(p[x])

    money = 10000
    stock = 0
    m = 0
    n = 0
    k = 0
    selltime = 3
    price = 0

    for x in range(len(interes)):
        print(interes[x])
        price = interes[x][1]
        if interes[x][2] == 'Buy ' and money != 0:
            stock += money / price
            money = 0
            m += 1
            print("----------------------------------\n",stock,money,price,"\n----------------------------------")
            k = 0 
        if interes[x][2] == 'Sell' and stock != 0:
            if selltime == 2:
                if k == 0:
                    money += price*stock*(0.5)
                    stock = stock * 0.5
                    k += 1
                else:
                    money += price*stock
                    stock = 0
                    k = 0
                n += 1
            if selltime == 3:
                if k == 0:
                    money += price*stock*(0.66)
                    stock = stock * 0.66
                    k += 1
                elif k == 1:
                    money += price*stock*(0.5)
                    stock = stock * 0.5
                    k += 1
                else:
                    money += price*stock
                    stock = 0
                    k = 0
            print("----------------------------------\n",stock,money,price,k,"\n----------------------------------")

        # if x == 30:
        #     break
    print(m,n)
    if stock == 0:
        print("You don't have stock. You have money",money)
    else:
        print("You have",stock,"stock Worth ",stock*price)









import PredicTrade as pt
import datetime

p = pt.predic("AAV")

# datetime yyyy mm dd
fdate = datetime.date(2017, 12, 1)
ldate = datetime.date(2018, 3, 20)
now = datetime.datetime.now().date()

if fdate > now:
    fdate = now
if ldate > now:
    ldate = now
ft = 0
lt = 0
if fdate != now and ldate != now:
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
    for x in range(len(interes)):
        print(interes[x])
        price = interes[x][1]
        if interes[x][2] == 'Buy ' and money != 0:
            stock += money / price
            money = 0
            m += 1
        if interes[x][2] == 'Sell' and stock != 0:
            if k == 0:
                money += price*stock*(0.5)
                stock = stock * 0.5
                k += 1
            else:
                money += price*stock
                stock = 0
                k = 0
            n += 1
        # if x == 30:
        #     break
    print(m,n)
    print(stock,money,price)
    









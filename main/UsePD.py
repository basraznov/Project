import format as gf
import sys
import PredicTrade as pt
import datetime

def getAllLastpredic():
    symbol = gf.allSymbol()
    w = symbol.index('MANRIN')
    # print(w)
    allLast = []
    temp = []
    k = None
    m = 0
    n = 0
    now = datetime.datetime.now().date()
    for x in range(len(symbol)):
        # print(symbol[x])
        sys.stdout.write("Download progress: %.2f%%   \r" % (x*100/len(symbol)) )
        sys.stdout.flush()
        temp = pt.predic(symbol[x])
        if temp == None:
            continue
        temp2 = temp[-1]
        if (temp2[0] - now).days > 3:
            continue
        if temp2[2] != "Hold":
            k = [symbol[x],temp2[2]]
            allLast.append(k)
            n += 1
        if temp2[2] == "Hold":
            m += 1

    #     print([symbol[x],temp2[2]])
    print(allLast)
    if not allLast:
        file = open('PD.txt','w')
        file.write("None")
    else:
        file = open('PD.txt','w')
        file.write(str(allLast))
    
getAllLastpredic()

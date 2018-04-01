def getAllLastpredic():
    symbol = gf.allSymbol()
    w = symbol.index('MANRIN')
    # print(w)
    allLast = []
    temp = []
    k = None
    now = datetime.datetime.now().date()
    for x in range(315,len(symbol)):
        # print(symbol[x])
        # sys.stdout.write("Download progress: %.2f%%   \r" % (x*100/len(symbol)) )
        # sys.stdout.flush()
        temp = predic(symbol[x])
        if temp == None:
            continue
        temp2 = temp[-1]
        if (temp2[0] - now).days > 3:
            continue
        if temp2[2] != "Hold":
            k = [symbol[x],temp2[2]]
            allLast.append(k)
            print("asdasd")
        print([symbol[x],temp2[2]])
    file = open('PD.txt','w')
    file.write(str(allLast))
    
getAllLastpredic()

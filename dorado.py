import requests
from datetime import datetime
from proxy_credenciales import proxy

def req_dorado():

    dorado=requests.get("https://sb2frontend-altenar2.biahosted.com/api/widget/GetEvents?culture=es-ES&timezoneOffset=300&integration=doradobet&deviceType=1&numFormat=en-GB&countryCode=PE&eventCount=0&sportId=0&champIds=3147",proxies=proxy)

    dic=dorado.json()
    
    mapeo={}
    conteo=0

    for i in dic["markets"]:
        if(i["name"]=="1x2"): 
            for j in i["oddIds"]: mapeo[j]=conteo
            conteo+=1

    diferente=0
    temp=[]
    total=[]

    for i in dic["odds"]:
        if(i["id"] in mapeo):
            if(mapeo[i["id"]]!=diferente):
                diferente=mapeo[i["id"]]
                total.append(temp)
                temp=[(i["price"],i["name"])]
            else: 
                temp.append((i["price"],i["name"]))
    
    total.append(temp)

    arr=[]

    for i in total:
        print(i)
        arr.append([str(datetime.now()),i[0][1],i[2][1],i[0][0],i[1][0],i[2][0]])

    return arr
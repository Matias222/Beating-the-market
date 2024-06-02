import requests
from datetime import datetime
from proxy_credenciales import proxy

def req_apuesta_total():

    apuesta_total=requests.get("https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=300&langId=4&skinName=apuestatotal1&configId=1&culture=es-ES&countryCode=PE&deviceType=Mobile&numformat=en&integration=apuestatotal1&sportids=66&categoryids=0&champids=3147&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2024-05-27T02%3A09%3A00.000Z&endDate=2024-06-03T02%3A09%3A00.000Z",proxies=proxy)

    dic=apuesta_total.json()
    arr=[]

    for i in dic["Result"]["Items"][0]["Events"]:
        
        print("-"*50)
        print(i["Name"])
        
        equipo_a=i["Items"][0]["Items"][0]["Name"]
        equipo_x=i["Items"][0]["Items"][1]["Name"]
        equipo_b=i["Items"][0]["Items"][2]["Name"]
        cuota_a=i["Items"][0]["Items"][0]["Price"]
        cuota_x=i["Items"][0]["Items"][1]["Price"]
        cuota_b=i["Items"][0]["Items"][2]["Price"]

        print(equipo_a,cuota_a)
        print(equipo_x,cuota_x)
        print(equipo_b,cuota_b)
        print(1/cuota_a+1/cuota_x+1/cuota_b)

        print("-"*50)
        print()

        arr.append([str(datetime.now()),equipo_a,equipo_b,cuota_a,cuota_x,cuota_b])
    
    return arr   

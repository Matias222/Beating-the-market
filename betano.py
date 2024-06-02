import requests
from datetime import datetime
from proxy_credenciales import proxy

def req_betano():

    arr=[]

    cabeza={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
    }
    q=requests.get("https://www.betano.pe/api/sport/futbol/campeonatos/copa-america/188650/?req=la,s,stnf,c,mb,mbl",headers=cabeza,proxies=proxy)
    data=q.json()

    for i in data["data"]["blocks"][0]["events"]:
        print("-"*50)

        for j in i["markets"][0]["selections"]:
            print(j["fullName"],j["price"])
        

        arr.append([str(datetime.now()),i["markets"][0]["selections"][0]["fullName"],i["markets"][0]["selections"][2]["fullName"],i["markets"][0]["selections"][0]["price"],i["markets"][0]["selections"][1]["price"],i["markets"][0]["selections"][2]["price"]])
        #print(i["name"])
        print("-"*50)

    return arr
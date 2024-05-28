from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests, time

def zz():
    payload={"LanguageId":11,"ClientTypeId":2,"BrandId":3,"JurisdictionId":2,"ClientIntegratorId":1,"ExternalIds":[13432238,12775282,12775283,12775284],"MarketCName":"win-draw-win","ScoreboardRequest":{"ScoreboardType":3,"IncidentRequest":{}},"BrowserId":3,"OsId":3,"ApplicationVersion":"","BrowserVersion":"125.0.0.0","OsVersion":"NT 10.0","SessionId":None,"TerritoryId":172,"CorrelationId":"4d6b067c-e129-4bea-ab04-07c0d8408c46","VisitId":"0c842aa8-087f-4a0a-bf4c-a0bf9fe604f3","ViewName":"sports","JourneyId":"0d1df9ca-d6e0-4038-80a4-e5d27e99ff5a"}
    cabeza={
        "Accept":"application/json; charset=UTF-8",
		"Accept-Encoding":"gzip, deflate, br, zstd",
		"Accept-Language":"en-US,en;q=0.5",
        "Connection":"keep-alive",
		#"Content-Length":"553"
		"Content-Type":"application/json; charset=UTF-8",
		"Cookie":"StaticResourcesVersion=24.05.0-22CC8FD7471A9947BA7C1C; ssc_btag=37c08b18-733b-4ed1-8a5c-70945d65ce33; TrackingVisitId=37c08b18-733b-4ed1-8a5c-70945d65ce33; ssc_DeviceId=be4d1ad4-0485-434d-873b-9a1c0764b139; ssc_DeviceId_HttpOnly=be4d1ad4-0485-434d-873b-9a1c0764b139; SpinSportVisitId=682554e9-d8f9-46a3-8b68-88e10751c8be; userLanguage=es; bw_BrowserId=26847382990757995280262093729106709361; bw_SessionId=51f59b4b-b109-4a46-a762-c252ee5ce109; ens_firstPageView=false; _scid=cf81685b-e091-4601-aff7-28728fdbf56e; _gcl_au=1.1.1959614822.1716784203; _ga=GA1.1.137249070.1716784204; _gid=GA1.2.1518972117.1716784204; ens_lobby_country=Peru; AMCV_74756B615BE2FD4A0A495EB8%40AdobeOrg=359503849%7CMCIDTS%7C19871%7CMCMID%7C36623361240682956482172876843666766681%7CMCAAMLH-1717389060%7C4%7CMCAAMB-1717389060%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCCIDH%7C-633572830%7CMCOPTOUT-1716791460s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.0.1; _cq_duid=1.1716784207.EUQuCygp0XHBtthJ; _cq_suid=1.1716784207.T9Vf1q1qWTZbL3Bk; AMCVS_74756B615BE2FD4A0A495EB8%40AdobeOrg=1; gpv_pn=%3Atbd%3Asports%3Asct%3Asoccer%3Acopa-america-2024; _fbp=fb.1.1716784207703.763200507; s_ecid=MCMID%7C36623361240682956482172876843666766681; ens_firstVisit=1716784260544; ens_firstVisitFlag=1; s_cc=true; _scid_r=cf81685b-e091-4601-aff7-28728fdbf56e; _sctr=1%7C1716699600000; _ga_HH1EZEXGZB=GS1.1.1716784260.1.0.1716784260.0.0.0; _rdt_uuid=1716784207217.ca5f0a04-fa89-4a60-8557-3cabde45b15d; _gat_UA-1515961-1=1",
		"Host":"sportsapi.betway.com",
		"Origin":"https://betway.com",
		"Priority":"u=1",
		"Referer":"https://betway.com/",
		"Sec-Fetch-Dest":"empty",
		"Sec-Fetch-Mode":"cors",
		"Sec-Fetch-Site":"same-site",
		"TE":"trailers",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
	}

    betway=requests.post("https://sportsapi.betway.com/api/Events/v2/GetEvents",headers=cabeza,json=payload)

    print(betway.content)

def req_apuesta_total():

    apuesta_total=requests.get("https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=300&langId=4&skinName=apuestatotal1&configId=1&culture=es-ES&countryCode=PE&deviceType=Mobile&numformat=en&integration=apuestatotal1&sportids=66&categoryids=0&champids=3147&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2024-05-27T02%3A09%3A00.000Z&endDate=2024-06-03T02%3A09%3A00.000Z")

    dic=apuesta_total.json()

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

def req_dorado():

    dorado=requests.get("https://sb2frontend-altenar2.biahosted.com/api/widget/GetEvents?culture=es-ES&timezoneOffset=300&integration=doradobet&deviceType=1&numFormat=en-GB&countryCode=PE&eventCount=0&sportId=0&champIds=3147")

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

    for i in total:
        print(i)

def req_betway():


    options = webdriver.ChromeOptions()
    options.set_capability(
            "goog:loggingPrefs", {"performance": "ALL"}
        )
    driver = webdriver.Chrome(options=options)

    driver.get("https://betway.com/es/sports/sct/soccer/copa-america-2024")

    time.sleep(10)

    actions = ActionChains(driver)

    sopa = BeautifulSoup(driver.page_source, "html.parser")
    div_elementos=sopa.find_all('div',{'data-widget':"""EventTableListWidget[soccer_copa-america-2024_matches, soccer_copa-america-2024_matches]""",'class':"eventTableItemCollection"})
    numero_iter = len(div_elementos[0].find_all('div', recursive=False))


    for i in range(4,numero_iter):

        xpath = f"/html/body/div[1]/div/div[3]/div/div[1]/div/div[2]/div[4]/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[{i+1}]"
        xpath = '/html/body/div[1]/div/div[3]/div/div[1]/div/div[2]/div[4]/div/div[2]/div/div[1]/div/div/div/div[2]/div/div[5]'
        element=driver.find_elements(By.XPATH, xpath)
        print(len(element))
        for j in element:

            actions.move_to_element(j).click().perform()

        print(i)

        time.sleep(30)

        time.sleep(0.1)


    time.sleep(20)


#req_apuesta_total()
#req_dorado()
req_betway()



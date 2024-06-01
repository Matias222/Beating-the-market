from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from escribir_csv import append_csv
from datetime import datetime
from bs4 import BeautifulSoup

import requests, time

def extraer_fecha(cadena):
    temp=""
    for i in range(len(cadena)-1,-1,-1):
        if(cadena[i]=="_"): return temp
        temp=cadena[i]+temp

def get_item(cadena):
    retornar=""
    temp=0
    bloqueo='collectionitem="'
    for i in range(len(cadena)):
        if(temp==len(bloqueo)):
            if(cadena[i]=='"'):
                if(len(retornar)==0): 
                    temp=0
                    continue
                else: return retornar
            retornar+=cadena[i]  
        else:
            if(cadena[i]==bloqueo[temp]): temp+=1
            else: temp=0

def req_apuesta_total():

    apuesta_total=requests.get("https://sb2frontend-altenar2.biahosted.com/api/Sportsbook/GetEvents?timezoneOffset=300&langId=4&skinName=apuestatotal1&configId=1&culture=es-ES&countryCode=PE&deviceType=Mobile&numformat=en&integration=apuestatotal1&sportids=66&categoryids=0&champids=3147&group=AllEvents&period=periodall&withLive=false&outrightsDisplay=none&marketTypeIds=&couponType=0&marketGroupId=0&startDate=2024-05-27T02%3A09%3A00.000Z&endDate=2024-06-03T02%3A09%3A00.000Z")

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
        
    append_csv("at",arr)

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

    arr=[]

    for i in total:
        print(i)
        arr.append([str(datetime.now()),i[0][1],i[2][1],i[0][0],i[1][0],i[2][0]])

    append_csv("dorado",arr)


def req_betway():


    enable_cursor = """
        function enableCursor() {
          var seleniumFollowerImg = document.createElement("img");
          seleniumFollowerImg.setAttribute('src', 'data:image/png;base64,'
            + 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAeCAQAAACGG/bgAAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAA'
            + 'HsYAAB7GAZEt8iwAAAAHdElNRQfgAwgMIwdxU/i7AAABZklEQVQ4y43TsU4UURSH8W+XmYwkS2I0'
            + '9CRKpKGhsvIJjG9giQmliHFZlkUIGnEF7KTiCagpsYHWhoTQaiUUxLixYZb5KAAZZhbunu7O/PKf'
            + 'e+fcA+/pqwb4DuximEqXhT4iI8dMpBWEsWsuGYdpZFttiLSSgTvhZ1W/SvfO1CvYdV1kPghV68a3'
            + '0zzUWZH5pBqEui7dnqlFmLoq0gxC1XfGZdoLal2kea8ahLoqKXNAJQBT2yJzwUTVt0bS6ANqy1ga'
            + 'VCEq/oVTtjji4hQVhhnlYBH4WIJV9vlkXLm+10R8oJb79Jl1j9UdazJRGpkrmNkSF9SOz2T71s7M'
            + 'SIfD2lmmfjGSRz3hK8l4w1P+bah/HJLN0sys2JSMZQB+jKo6KSc8vLlLn5ikzF4268Wg2+pPOWW6'
            + 'ONcpr3PrXy9VfS473M/D7H+TLmrqsXtOGctvxvMv2oVNP+Av0uHbzbxyJaywyUjx8TlnPY2YxqkD'
            + 'dAAAAABJRU5ErkJggg==');
          seleniumFollowerImg.setAttribute('id', 'selenium_mouse_follower');
          seleniumFollowerImg.setAttribute('style', 'position: absolute; z-index: 99999999999; pointer-events: none; left:0; top:0');
          document.body.appendChild(seleniumFollowerImg);
          document.onmousemove = function (e) {
            document.getElementById("selenium_mouse_follower").style.left = e.pageX + 'px';
            document.getElementById("selenium_mouse_follower").style.top = e.pageY + 'px';
          };
        };

        enableCursor();
    """


    options = webdriver.ChromeOptions()
    options.set_capability(
            "goog:loggingPrefs", {"performance": "ALL"}
        )

    driver = webdriver.Chrome(options=options)

    driver.get("https://betway.com/es/sports/sct/soccer/copa-america-2024")
        
    #time.sleep(10)

    actions = ActionChains(driver)
    driver.execute_script(enable_cursor)    

    css_selector="""div[data-tap-recogniser="true"].cookiePolicyAcceptButton"""

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
    )

    element.click()
    
    time.sleep(3.5)

    sopa = BeautifulSoup(driver.page_source, "html.parser")
    div_elementos=sopa.find_all('div',{'data-widget':"""EventTableListWidget[soccer_copa-america-2024_matches, soccer_copa-america-2024_matches]""",'class':"eventTableItemCollection"})
    div_elementos=div_elementos[0].find_all('div', recursive=False)

    print("LISTO")

    for i in range(3,len(div_elementos)):
        
        item=get_item(str(div_elementos[i]))
        
        element = driver.find_element(By.CSS_SELECTOR,f"""div[collectionitem="{item}"].collapsablePanel""")
        actions.move_to_element(element).click().perform()
        print(i)

        time.sleep(1)

    sopa = BeautifulSoup(driver.page_source, "html.parser")
    arr=[]

    for i in div_elementos:
        
        fecha=extraer_fecha(get_item(str(i)))
        
        partidos=sopa.find_all('div',{'data-tap-recogniser':"true",'class':"eventItemCollection","data-widget":f"EventListWidget[soccer_copa-america-2024_matches, {fecha}]"})
        partidos_ids=partidos[0].find_all('div', recursive=False)

        for j in partidos_ids:
            
            extraer_id=get_item(str(j))
            nombres=j.find('div',{'class':"oneLineScoreboard soccer upcoming","data-widget":f"EventSummaryWidget[soccer_copa-america-2024_matches, {extraer_id}]"})
            
            home=nombres.find('span',{'class':"teamNameFirstPart teamNameHomeTextFirstPart"}).text
            away=nombres.find('span',{'class':"teamNameFirstPart teamNameAwayTextFirstPart"}).text

            cuotas=j.find_all('div',{'class':"odds"})

            print()
            print(home,cuotas[0].text)
            print("X",cuotas[1].text)
            print(away,cuotas[2].text)
            print()

            arr.append([str(datetime.now()),home,away,cuotas[0].text,cuotas[1].text,cuotas[2].text])
    
    append_csv("betway",arr)

    #time.sleep(100)
    return

def req_betano():

    arr=[]

    cabeza={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
    }
    q=requests.get("https://www.betano.pe/api/sport/futbol/campeonatos/copa-america/188650/?req=la,s,stnf,c,mb,mbl",headers=cabeza)
    data=q.json()

    for i in data["data"]["blocks"][0]["events"]:
        print("-"*50)

        for j in i["markets"][0]["selections"]:
            print(j["fullName"],j["price"])
        

        arr.append([str(datetime.now()),i["markets"][0]["selections"][0]["fullName"],i["markets"][0]["selections"][2]["fullName"],i["markets"][0]["selections"][0]["price"],i["markets"][0]["selections"][1]["price"],i["markets"][0]["selections"][2]["price"]])
        #print(i["name"])
        print("-"*50)

    append_csv("betano",arr)

#    print(q.json())


#req_apuesta_total()
#req_dorado()
#req_betano()
req_betway()

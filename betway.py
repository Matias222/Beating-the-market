from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy

from bs4 import BeautifulSoup
from proxy_credenciales import proxy,proxy_url,proxy_host, proxy_password, proxy_username


import requests, time
from datetime import datetime

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

    options.add_argument("--headless=new")
    options.add_argument('disable-gpu')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")


    proxy_helper = SeleniumAuthenticatedProxy(proxy_url=proxy_url)
    proxy_helper.enrich_chrome_options(options)


    driver = webdriver.Chrome(options=options)

    driver.get("https://betway.com/es/sports/sct/soccer/copa-america-2024")
    
    time.sleep(15)
    
    print(driver.page_source)

    actions = ActionChains(driver)
    driver.execute_script(enable_cursor)    

    css_selector="""div[data-tap-recogniser="true"].cookiePolicyAcceptButton"""

    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
    )

    element.click()

    time.sleep(15)

    sopa = BeautifulSoup(driver.page_source, "html.parser")
    div_elementos=sopa.find_all('div',{'data-widget':"""EventTableListWidget[soccer_copa-america-2024_matches, soccer_copa-america-2024_matches]""",'class':"eventTableItemCollection"})
    div_elementos=div_elementos[0].find_all('div', recursive=False)

    print("LISTO",len(div_elementos))

    for i in range(3,len(div_elementos)):
        
        item=get_item(str(div_elementos[i]))
        
        element = driver.find_element(By.CSS_SELECTOR,f"""div[collectionitem="{item}"].collapsablePanel""")
        actions.move_to_element(element).click().perform()
        print(i)

        time.sleep(2)

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
    
    return arr

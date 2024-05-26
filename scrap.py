from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import json
import time

def log_filter(log_):
    return (log_["method"] == "Network.responseReceived" and "json" in log_["params"]["response"]["mimeType"])

def devolver_id(cadena):
    arr = cadena.split('/')
    return arr[-2]

def get_link(cadena):
    retornar=""
    temp=0
    bloqueo='/football/world/world-championship-2022/'
    for i in range(len(cadena)):
        if(temp==len(bloqueo)):
            if(cadena[i]=='"'):
                if(len(retornar)==0): 
                    temp=0
                    continue
                else: return bloqueo+retornar
            retornar+=cadena[i]  
        else:
            if(cadena[i]==bloqueo[temp]): temp+=1
            else: temp=0

def extraer_llave(cadena):

    bloqueo=0
    temp=""

    for i in range(len(cadena)-1,-1,-1):
        
        if(bloqueo==1):
            if(cadena[i]=="/"): return "".join(reversed(temp))
            else: temp+=cadena[i]
            bloqueo=1
        elif(cadena[i]=="-"): bloqueo=1


def scrap(driver):
        
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

    sopa = BeautifulSoup(driver.page_source, "html.parser")

    div_elements = sopa.find_all('div', class_='eventRow flex w-full flex-col text-xs')
    
    print(div_elements)
    
    
    links=[]
    fecha_tipo=[]
    paises=[]
    resultado=[]

    for i in div_elements: 

        links.append(get_link(str(i)))
        buscar_fecha = i.find_all('div',class_="text-black-main font-main w-full truncate text-xs font-normal leading-5")
        buscar_nombre = i.find_all('p',{'data-v-67b8c018':'','class':"participant-name truncate"})

        paises.append((buscar_nombre[0].text,buscar_nombre[1].text))
        
        if(len(buscar_fecha)!=0): fecha_tipo.append((buscar_fecha[0]).text)
        else: fecha_tipo.append(fecha_tipo[-1])

    for i in range(len(links)): 
        print("-"*50)
        print(links[i],fecha_tipo[i])#,paises[i][0]+"-"+paises[i][1])
        print(paises[i][0]+"-"+paises[i][1])
        #print(resultado[i])
        print("-"*50)


    for i in links:

        driver.get("https://www.oddsportal.com"+i)
        time.sleep(1.8)

        sopa = BeautifulSoup(driver.page_source, "html.parser")
        marcador_a = sopa.find('div',class_="text-gray-dark flex w-full flex-wrap gap-2").text
        marcador_b = sopa.find('div',class_="flex-center text-gray-dark flex-wrap gap-2 max-sm:mr-0").text
        div_elements = sopa.find_all('div', class_='border-black-borders flex h-9 border-b border-l border-r text-xs')
        llave_data=extraer_llave(i)

        resultado.append((marcador_a,marcador_b))

        dic={}

        for j in div_elements:
            
            url_img = j.find('img', {'data-v-155f876a': ''})
            dic[url_img.get('title')]=devolver_id(url_img.get('src'))

        logs_raw = driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

        for log in filter(log_filter, logs):
            resp_url = log["params"]["response"]["url"]
        
            if(resp_url[-2:]=="en"): api_cuotas=resp_url
        
        print(api_cuotas)

        driver.get(api_cuotas)
    
        sopa= BeautifulSoup(driver.page_source, 'html.parser')
        dic_cuotas = json.loads(sopa.find('pre').text)

        print()

        for j in dic:

            arr_casa=dic_cuotas["d"]["oddsdata"]["back"]["E-1-2-0-0-0"]["odds"][str(dic[j])]
            arr_casa_opening=dic_cuotas["d"]["oddsdata"]["back"]["E-1-2-0-0-0"]["openingOdd"][str(dic[j])]
    
            #print(arr_casa)
            #print(arr_casa_opening)

            with open("./data_2022/"+str(j)+".csv",'a') as f: 
                
                f.write(f"{llave_data},{arr_casa['0']},{arr_casa['1']},{arr_casa['2']},{arr_casa_opening['0']},{arr_casa_opening['1']},{arr_casa_opening['2']}")
                f.write('\n')

        if(llave_data=="qatar-ecuador"): break
    
    for i in range(len(resultado)): 

        with open("./data_2022/todo.csv",'a') as f: 
            
            dividir=fecha_tipo[i].split("-")
            
            if(len(dividir)==1): dividir.append("Groups") 

            f.write(f"{extraer_llave(links[i])},{paises[i][0]},{paises[i][1]},{dividir[0]},{dividir[1]},{resultado[i][0]},{resultado[i][1]}")
            f.write("\n")

        #print("-"*50)
        #print(links[i],fecha_tipo[i])#,paises[i][0]+"-"+paises[i][1])
        #print(paises[i][0]+"-"+paises[i][1])
        #print(resultado[i])
        #print("-"*50)


options = webdriver.ChromeOptions()
options.set_capability(
            "goog:loggingPrefs", {"performance": "ALL"}
        )
driver = webdriver.Chrome(options=options)

driver.get('https://www.oddsportal.com/football/world/world-championship-2022/results/')
scrap(driver)
driver.get('https://www.oddsportal.com/football/world/world-championship-2022/results//#/page/2')
scrap(driver)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from escribir_csv import append_csv
from datetime import datetime
from bs4 import BeautifulSoup
from proxy_credenciales import proxy,proxy_url,proxy_host, proxy_password, proxy_username


import requests, time, pyautogui








#    print(q.json())

#req_apuesta_total()
#req_dorado()
#req_betano()
req_betway()

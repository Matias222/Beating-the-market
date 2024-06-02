import requests
import random

proxy_username = "brd-customer-hl_4f29b07f-zone-datacenter_proxy1"
proxy_password = "tfpwy4ggrik9"
proxy_host = "brd.superproxy.io:22225"
session_id = random.random()

proxy_url = f'http://{proxy_host}'

print(proxy_url)

proxy = {'http': proxy_url, 'https': proxy_url}

arr = []

cabeza = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
}
q = requests.get(
    "https://www.betano.pe/api/sport/futbol/campeonatos/copa-america/188650/?req=la,s,stnf,c,mb,mbl",
    headers=cabeza,
    proxies=proxy)

print(q.status_code)
data = q.json()

print(data)

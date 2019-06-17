
# pip install scapy
# pip install requests

from scapy.all import *
import requests
import json
import sys
import socket

# Signup at https://www.ipdata.co/sign-up.html to get a 1500 free request api key
api_key="xxxxx"

def api_lookup(ip,latency):
    response = requests.get('https://api.ipdata.co/'+ip+"?api-key="+api_key)
    binary = response.content
    output = json.loads(binary)

    if response.status_code == 403:
        print("Please check api code/quota")
        return 0
    elif response.status_code == 200:
        if output['organisation'] is None:
            org = "N.A"
        else:
            org = output['organisation']

        if output['asn'] is None:
            asn = "N.A"
        else:
            asn = output['asn']

        print("{0:<20} {1:<7.2f}ms {2:3<}  {3:<15}  {4:10}".format(ip,latency," ",asn,org))

                
    else:
        print("Unknown error with API")
        return 0

def icmp_trace(host):
    print ("----------------------------------------------------------------------------")
    print("Tracroute " + host)
    print ("----------------------------------------------------------------------------")
    print("{0:<20} {1:<9} {2:3<}  {3:<15}  {4:10}".format("HOP","latency"," ","asn","org"))
    print ("----------------------------------------------------------------------------")
    flag = True
    ttl=2
    i=0
    hops = []

    while flag and i<30:

        ans, unans = sr(IP(dst=host,ttl=ttl)/ICMP(id=1),verbose=0,timeout=1,retry=0)

        if len(ans) == 1:
            rx = ans[0][1]
            tx = ans[0][0]
            delta=(rx.time-tx.sent_time)*1000
            if ans.res[0][1].type == 0: # checking for  ICMP echo-reply
                    flag = False
                    api_lookup(ans.res[0][1].src,delta)
            else:
                    api_lookup(ans.res[0][1].src,delta)
                    ttl +=1
                    i +=1
        else:
            ttl +=1
            i +=1
            print("No answer from hop")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        icmp_trace(sys.argv[1])
    elif len(sys.argv) == 1:

        host = input("Enter hostname/IP: ")
        ip=socket.gethostbyname(host)
        icmp_trace(ip)
        print ("----------------------------------------------------------------------------")
    else:
        print("ERROR: usage asn_traceroute.py [hostname/ip]")
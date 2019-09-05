# Dependencies:
# pip install scapy
# pip install requests
# pip install netaddr

from os import system, name
from netaddr import * 
import requests
import json
import sys
import re

# Signup at https://www.ipdata.co/sign-up.html to get a 1500 free request api key
api_key="504c83ed61956cee4bfffd0f4d874d1086fc5dc2e0d1fb322d8f5db6"

def api_lookup(ip):

    #check if IP is from private range (except from AS lookup)
    if not IPAddress(ip).is_private():

        #generate web request against api
        response = requests.get('https://api.ipdata.co/'+ip+"?api-key="+api_key)
        binary = response.content
        output = json.loads(binary)

        #check retrun code of web request
        #request went wrong because api code was wrong or over quota
        if response.status_code == 403:
            print("Please check api code/quota")

        #request was ok
        elif response.status_code == 200:
            if output['organisation'] is None:
                org = "N.A"
            else:
                org = output['organisation']

            if output['asn'] is None:
                asn = "N.A"
            else:
                asn = output['asn']

            #return string with asn and org
            return asn+" / "+org

        #uknown retunr code from web request was received
        else:
            return "Unknown error with API"
    else:
        #return string
        return "PRIVATE IP"

def clear(): 
    # windows
    if name == 'nt': 
        _ = system('cls') 
    # *nix 
    else: 
        _ = system('clear') 

# main function
if __name__ == '__main__':
    lines = []
    i=0
    j=0

    # Read input line
    print("############### AS LOOKUP TOOL - BY PAUL FREITAG ##########")
    print("Please copy the output that contains the IPs that should be looked up. If finshed please end input with empty line only containing ")
    print("INPUT:")
    while True:
        #read until line with only . appears
        line = input()
        if line != ".":
            lines.append(line)
            i += 1
        else:
            break

    # Output
    #clear console output
    clear()
    print("============ RESULT =============")
    while j < i:
        #search for IP pattern
        IP = re.search(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', lines[j])
        #IP found
        if IP is not None:
            #make api call for BGP AS info and build replacement string
            NEW_IP_STRING = IP.group() + " (" + api_lookup(IP.group()) + ")"
            #replace ip with ip and ASN information
            REPLACED_IP = re.sub(IP.group(),NEW_IP_STRING,lines[j])
            print(REPLACED_IP)
        #no ip found
        else:
            print(lines[j])
        j +=1
 
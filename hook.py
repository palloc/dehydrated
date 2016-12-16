#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import sys
import time

f = open("APIfile.data", "r")
user, password = f.read().split('\n')
zone = ''




# Create subdomain for DNS auth
def Create_Domain(name):
    zone_tmp = name.split(".")
    zone = zone_tmp[-2] + "." + zone_tmp[-1]
    return "_acme-challenge." + name.replace("."+zone, "")
    



# Get url of service information
def Get_Info_URL():
    get_id_url = 'https://secure.sakura.ad.jp/cloud/zone/is1a/api/cloud/1.1/commonserviceitem'

    try:
        tmp = requests.get(get_id_url, auth=(user, password)).json()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

        
    # Get info url
    num = 0
    for i in range(len(tmp["CommonServiceItems"])):
        if tmp["CommonServiceItems"][i]["Status"]["Zone"] == zone:
            num = i
    id = tmp["CommonServiceItems"][num]["ID"]

    return get_id_url+"/"+id





# Get post data from info_url
def Gen_Postdata(info_url):
    try:
        data = requests.get(info_url, auth=(user, password)).json()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
        

    del data["is_ok"], \
        data["CommonServiceItem"]["ID"], \
        data["CommonServiceItem"]["Name"], \
        data["CommonServiceItem"]["Description"], \
        data["CommonServiceItem"]["SettingsHash"], \
        data["CommonServiceItem"]["ServiceClass"], \
        data["CommonServiceItem"]["Status"], \
        data["CommonServiceItem"]["Availability"], \
        data["CommonServiceItem"]["CreatedAt"], \
        data["CommonServiceItem"]["ModifiedAt"], \
        data["CommonServiceItem"]["Provider"], \
        data["CommonServiceItem"]["Icon"], \
        data["CommonServiceItem"]["Tags"] 
    
    return data





# Deploy Challenge
if sys.argv[1] == "deploy_challenge":
    domain = Create_Domain(sys.argv[2])
    print("domain = "+domain)
    
    info_url = Get_Info_URL()
    post_data = Gen_Postdata(info_url)



    # Add TXT record to post data
    post_data["CommonServiceItem"]["Settings"]["DNS"]["ResourceRecordSets"] += [{"Name": domain, "Type": "TXT", "RData": sys.argv[4], "TTL": 600}]



    # Regist TXT record
    try:
        res = requests.put(info_url, \
                            json.dumps(post_data), \
                            auth=(user, password), \
                            headers={'Content-Type': 'application/json'})
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    print("post data = "+json.dumps(post_data))
    time.sleep(60)
    print("fin deploy.")
    




# Clean Challenge
elif sys.argv[1] == "clean_challenge":
    domain = Create_Domain(sys.argv[2])

    info_url = Get_Info_URL()
    post_data = Gen_Postdata(info_url)

    num = 0
    for i in range(len(post_data["CommonServiceItem"]["Settings"]["DNS"]["ResourceRecordSets"])):
        if domain in post_data["CommonServiceItem"]["Settings"]["DNS"]["ResourceRecordSets"][i]["Name"]:
            num = i

            
    # Delete _acme-challenge's TXT record
    del post_data["CommonServiceItem"]["Settings"]["DNS"]["ResourceRecordSets"][i]
    
    try:
        res = requests.put(info_url, \
                            json.dumps(post_data), \
                            auth=(user, password), \
                            headers={'Content-Type': 'application/json'})    
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    print("fin clean.")





# Deploy Cert    
elif sys.argv[1] == "deploy_cert":
    pass

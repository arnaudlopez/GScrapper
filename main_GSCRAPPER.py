#!/usr/bin/env python
# coding: utf-8
# By Arnaud LOPEZ, 2015

import logging, json, csv, codecs, time, urllib2
import geocoder
from importio import importio
from importio import latch
import mechanize
from bs4 import BeautifulSoup
import re
import pickle

name = "GMAPScrapper",
version = "0.1",
description = "Ce programme scrappe googlemaps V2",
autor = 'Arnaud LOPEZ',

global jsonDATA 

class VCards():
    def __init__(self, name, phoneNumber, address, web, mail):
        self.name = name
        self.phoneNumber = phoneNumber
        self.address = address
        self.web = web
        self.mail = mail



def getAPIGOOGLE(searchTerm, place, records):
    # To use an API key for authentication, use the following code:
    client = importio.importio(user_id="132bbe63-5552-41a2-ab3c-440ca93b8fa9", api_key="Ge28+Cy7Kxs8Z9gatZgj5BZv9MF8JwCpRxB97O1fwUgbv7kYXdgUQuE00fW4tTOi6HwEfPVlR2zAvfLdsI3QMQ==", host="https://query.import.io")
    
    # Once we have started the client and authenticated, we need to connect it to the server:
    client.connect()
    
    # Because import.io queries are asynchronous, for this simple script we will use a "latch"
    # to stop the script from exiting before all of our queries are returned
    # For more information on the latch class, see the latch.py file included in this client library
    queryLatch = latch.latch(1)
    
    # Define here a global variable that we can put all our results in to when they come back from
    # the server, so we can use the data later on in the script
    dataRows = []
    
    g = geocoder.google(place)
    
    # In order to receive the data from the queries we issue, we need to define a callback method
    # This method will receive each message that comes back from the queries, and we can take that
    # data and store it for use in our app
    def callback(query, message):

    
      # Disconnect messages happen if we disconnect the client library while a query is in progress
      if message["type"] == "DISCONNECT":
        print "Query in progress when library disconnected"
       # print json.dumps(message["data"], indent = 4)
    
      # Check the message we receive actually has some data in it
      if message["type"] == "MESSAGE":
        if "errorType" in message["data"]:
          # In this case, we received a message, but it was an error from the external service
          print "Got an error! API MAPS" 
          print json.dumps(message["data"], indent = 4)
        else:
          # We got a message and it was not an error, so we can process the data
          #print "Got data!"
         # print json.dumps(message["data"], indent = 4, encoding="utf-8", ensure_ascii=False)
          # Save the data we got in our dataRows variable for later
          dataRows.extend(message["data"]["results"])
      
      # When the query is finished, countdown the latch so the program can continue when everything is done
      if query.finished(): queryLatch.countdown()
    
    # Issue queries to your data sources and with your inputs
    # You can modify the inputs and connectorGuids so as to query your own sources
    # Query for tile Magic Api
    
    if lp==0:
        client.query({
          "connectorGuids": [
            "df114343-28c4-461a-a349-4a99e04c6a11"
          ],
          "input": {
            "webpage/url": "https://maps.google.fr/maps?sll="+str(g.lat)+","+str(g.lng)+"&q="+searchTerm+"&ie=UTF8&hl=fr&sspn=0.000000,0.000000&dg=brw&sa=N&start="+str(records)+"&output=classic"
          }
        }, callback)

    if lp==10:

        client.query({
          "connectorGuids": [
            "df114343-28c4-461a-a349-4a99e04c6a11"
          ],
          "input": {
            "webpage/url": ""+str(nextlink)+"&output=classic"+""
          }
        }, callback)
        
    if lp>10:
      
        client.query({
          "connectorGuids": [
            "df114343-28c4-461a-a349-4a99e04c6a11"
          ],
          "input": {
            "webpage/url": ""+str(nextlink)+"&output=classic"+""
          }
        }, callback)
        
        
   # print "Queries dispatched, now waiting for results"
    
    # Now we have issued all of the queries, we can "await" on the latch so that we know when it is all done
    queryLatch.await()
    
    #print "Latch has completed, all results returned"
    
    # It is best practice to disconnect when you are finished sending queries and getting data - it allows us to
    # clean up resources on the client and the server
    client.disconnect()
    
    # Now we can print out the data we got
   # print "All data received:"
   # print json.dumps(dataRows, indent = 4, ensure_ascii=False)
    return json.dumps(dataRows, indent = 4, ensure_ascii=False)
    
    

def getDATA():
    decoded = json.loads(jsonDATA)
    for vc in decoded:
        name = "none"
        phoneNumber = "none"
        address = "none"
        web = "none"
        mail = "none"
        try:
            name = vc['place_title_text']
            print name
            phoneNumber = vc['text_1'].replace(" ","").replace(",","")
            print phoneNumber
            address = vc['address_text'].replace(",","")
            print address
            web = vc['authority_page_link/_text'].replace(" ","").replace(",","")
            print web
            vc1 = VCards(name, phoneNumber, address, web, mail)
            vCardArray.append(vc1)
        except KeyError:
            print "ERROR"
            vc1 = VCards(name, phoneNumber, address, web, mail)
            vCardArray.append(vc1)
            continue
        

def initsoup():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-Agent','Google Chrome')]
    

def getmails():
    i=0
    webMail = ""
    
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-Agent','Google Chrome')]

    
    for loop in vCardArray:
        web = loop.web
        print web
        if web != "" and web != "," and web != "none":
            urls = "http://www."+str(web)+"/"
            print urls
            print web
            try:
                htmltext = br.open(urls,timeout=10.0).read()
                mails = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", htmltext)
                formattedMail = str(mails).replace(" ","").replace("[","").replace("]","").replace("',u'",",").replace("'","")
                webMails = re.split(',+', str(formattedMail))
                webMail = webMails[0]
            except mechanize.HTTPError, exc:
                print mechanize.HTTPError
                print exc.reason
                print urls
                print "170"
                continue
            except urllib2.URLError, e:
                bug = str(e.reason)
                if bug == "[Errno -2] Name or service not known" or bug == "Not Found":
                    try:
                        urls = "http://"+str(web)+"/"
                        htmltext = br.open(urls,timeout=7.0).read()
                        mails = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", htmltext)
                        formattedMail = str(mails).replace(" ","").replace("[","").replace("]","").replace("',u'",",").replace("'","")
                        webMails = re.split(',+', str(formattedMail))
                        webMail = webMails[0]
                    except urllib2.URLError, e:
                        print e.reason
                        print"203"
                        continue
         
            mails = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", htmltext)
            formattedMail = str(mails).replace(" ","").replace("[","").replace("]","").replace("',u'",",").replace("'","")
            webMails = re.split(',+', str(formattedMail))
            webMail = webMails[0]
            print webMail
            
            if webMail == "":
                soup = BeautifulSoup(htmltext)
                
                for link in soup.find_all('a'):
                    liens = link.get('href')
                    tpm = "none"
                    if liens == None: liens="none"
                    if liens[0:1] == "/": 
                        tmp = str(re.findall("contact", liens))
                     
                        if tmp == "['contact']":
                            url = "http://www."+str(web)+str(liens)
                            try:
                                print url+"210"
                                htmltext = br.open(url,timeout=5.0).read()
                                mails = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", htmltext)
                                formattedMail = str(mails).replace(" ","").replace("[","").replace("]","").replace("',u'",",").replace("'","")
                                webMails = re.split(',+', str(formattedMail))
                                webMail = webMails[0]
                            except mechanize.HTTPError, exc:
                                print  mechanize.HTTPError
                                print exc.reason
                                print"214"
                                continue
                            except urllib2.URLError, e:
                                bug = str(e.reason)
                                if bug == "[Errno -2] Name or service not known":
                                    try:
                                        url = "http://"+str(web)+str(liens)
                                        print url+"225"
                                        htmltext = br.open(url,timeout=5.0).read()
                                        mails = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", htmltext)
                                        formattedMail = str(mails).replace(" ","").replace("[","").replace("]","").replace("',u'",",").replace("'","")
                                        webMails = re.split(',+', str(formattedMail))
                                        webMail = webMails[0]
                                    except urllib2.URLError, e:
                                        print e.reason
                                        print "228"
                                continue

                    if liens[0:2] =="ht":
                        tmp = str(re.findall("contact", liens))
                        if tmp == "['contact']":
                            url = liens
                            try:
                                print url+"241"
                                htmltext = br.open(url,timeout=5.0).read()
                                mails = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", htmltext)
                                formattedMail = str(mails).replace(" ","").replace("[","").replace("]","").replace("',u'",",").replace("'","")
                                if mails != "":
                                    webMails = re.split(',+', str(formattedMail))
                                    webMail = webMails[0]
                            except mechanize.HTTPError, exc:
                                print  mechanize.HTTPError
                                print exc.reason
                                print "245"
                                continue
                            except urllib2.URLError, e:
                                bug = str(e.reason)
                                if bug == "[Errno -2] Name or service not known":
                                    try:
                                        url = "http://"+str(liens[8:])
                                        print url+"256"
                                        htmltext = br.open(url,timeout=5.0).read()
                                        mails = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", htmltext)
                                        formattedMail = str(mails).replace(" ","").replace("[","").replace("]","").replace("',u'",",").replace("'","")
                                        webMails = re.split(',+', str(formattedMail))
                                        webMail = webMails[0]
                                    except urllib2.URLError, e:
                                        print e.reason
                                        print "259"
                                        continue
                                continue
                            
                    if liens[0:2] !="ht" and liens[0:1] != "/" and liens[0:3] != "jav":
                        tmp = str(re.findall("contact", liens))
                        if tmp == "['contact']":
                            url = "http://www."+str(web)+"/"+str(liens)
                            try:
                                print url+"274"
                                htmltext = br.open(url,timeout=5.0).read()
                                mails = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", htmltext)
                                formattedMail = str(mails).replace(" ","").replace("[","").replace("]","").replace("',u'",",").replace("'","")
                                webMails = re.split(',+', str(formattedMail))
                                webMail = webMails[0]
                            except mechanize.HTTPError, exc:
                                print  mechanize.HTTPError
                                print exc.reason
                                continue
                            except urllib2.URLError, e:
                                bug = str(e.reason)
                                if bug == "[Errno -2] Name or service not known":
                                    try:
                                        url = "http://"+str(web)+"/"+str(liens)
                                        print url+"289"
                                        htmltext = br.open(url,timeout=5.0).read()
                                        mails = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", htmltext)
                                        formattedMail = str(mails).replace(" ","").replace("[","").replace("]","").replace("',u'",",").replace("'","")
                                        webMails = re.split(',+', str(formattedMail))
                                        webMail = webMails[0]
                                    except urllib2.URLError, e:
                                        print e.reason
                                        print "297"
                                        continue
                                continue
                            
            if webMail == "":
                webMail ="none"
        
            vCardArray[i].mail = webMail
        i += 1

def getNEXT(searchTerm, place, records):
 # To use an API key for authentication, use the following code:
    client = importio.importio(user_id="132bbe63-5552-41a2-ab3c-440ca93b8fa9", api_key="Ge28+Cy7Kxs8Z9gatZgj5BZv9MF8JwCpRxB97O1fwUgbv7kYXdgUQuE00fW4tTOi6HwEfPVlR2zAvfLdsI3QMQ==", host="https://query.import.io")
    
    # Once we have started the client and authenticated, we need to connect it to the server:
    client.connect()
    
    # Because import.io queries are asynchronous, for this simple script we will use a "latch"
    # to stop the script from exiting before all of our queries are returned
    # For more information on the latch class, see the latch.py file included in this client library
    queryLatch = latch.latch(1)
    
    # Define here a global variable that we can put all our results in to when they come back from
    # the server, so we can use the data later on in the script
    dataRows2 = []
    g = geocoder.google(place)
    # In order to receive the data from the queries we issue, we need to define a callback method
    # This method will receive each message that comes back from the queries, and we can take that
    # data and store it for use in our app
    def callback(query, message):
      global dataRows
      
      # Disconnect messages happen if we disconnect the client library while a query is in progress
      if message["type"] == "DISCONNECT":
        print "Query in progress when library disconnected"
        print json.dumps(message["data"], indent = 4)
    
      # Check the message we receive actually has some data in it
      if message["type"] == "MESSAGE":
        if "errorType" in message["data"]:
          # In this case, we received a message, but it was an error from the external service
            print "erreur link"
        else:
          # We got a message and it was not an error, so we can process the data

          dataRows2.extend(message["data"]["results"])
      
      # When the query is finished, countdown the latch so the program can continue when everything is done
      if query.finished(): queryLatch.countdown()
    
    # Issue queries to your data sources and with your inputs
    # You can modify the inputs and connectorGuids so as to query your own sources
    # Query for tile Magic Api
    if lp == 0:
        client.query({
          "connectorGuids": [
            "1f59482a-3c8e-479d-985e-daafe92e71a3"
          ],
          "input": {
            "webpage/url": "https://maps.google.fr/maps?sll="+str(g.lat)+","+str(g.lng)+"&q="+searchTerm+"&ie=UTF8&hl=fr&sspn=0.000000,0.000000&dg=brw&sa=N&start="+str(records)+"&output=classic&dg=brw"
                            
          }
        }, callback)
       
    if lp == 10:
        global nextlink
        print nextlink+str(lp)
        client.query({
          "connectorGuids": [
            "1f59482a-3c8e-479d-985e-daafe92e71a3"
          ],
          "input": {
            "webpage/url": ""+str(nextlink)+"&output=classic"+""
                           
          }
        }, callback)
        
    if lp > 10:
        global nextlink
        print nextlink+str(lp)
        client.query({
          "connectorGuids": [
            "1f59482a-3c8e-479d-985e-daafe92e71a3"
          ],
          "input": {
            "webpage/url": ""+str(nextlink)+"&output=classic"+""
                           
          }
        }, callback)    
        
  #  print "Queries dispatched, now waiting for results"
    
    # Now we have issued all of the queries, we can "await" on the latch so that we know when it is all done
    queryLatch.await()
    
  #  print "Latch has completed, all results returned"
    
    # It is best practice to disconnect when you are finished sending queries and getting data - it allows us to
    # clean up resources on the client and the server
    client.disconnect()
    
    # Now we can print out the data we got
  #  print "All data received:"
    jdata = json.dumps(dataRows2, indent = 4, ensure_ascii=False , encoding="utf8")
 
    decoded = json.loads(jdata)
  
    for vc in decoded:
        nextlink = vc['my_column']
    return nextlink

terme = raw_input("Terme de recherche ? ...\n->")
lieu = raw_input("Lieu de recherche ? ...\n->")
lp = 0

while lp <=190: 
    print lp
    vCardArray = []
    jsonDATA = getAPIGOOGLE(terme, lieu, lp)
    getDATA()
    initsoup()
    getmails()
 
    myfile = codecs.open("data.csv","a" ,"utf8")
    
    for vc in vCardArray: 
        #print vc.name, vc.phoneNumber, vc.address, vc.web, vc.mail
        myfile.write(vc.name+";"+vc.phoneNumber+";"+vc.address+";"+vc.web+";"+vc.mail+"\n")
    myfile.close()
 
    time.sleep(2)
    
    nextlink = getNEXT(terme, lieu, lp)
    lp+=10
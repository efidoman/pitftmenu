#!/usr/bin/python

import os, requests, json, pprint

#d=dict
res1=requests.get(os.environ["NIGHTSCOUT_HOST"] + '/api/v1/entries.json?count=1')
d=res1.json()
#pprint.pprint(d)
print d

if len(d) > 0:
    if 'glucose' in d[0]:
        print d[0]['glucose']
    else:
        print "Glucose not found in response to get entries"


#res2 = requests.get(os.environ["NIGHTSCOUT_HOST"] + '/api/v1/devicestatus?count=1')      
#data2=res2.json()
#pprint.pprint(data2)

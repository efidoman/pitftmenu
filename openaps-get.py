#!/usr/bin/python

import os, requests, json, pprint


def test():
    print "here 1"
    return
    print "here 2"

try:
    res1=requests.get(os.environ["NIGHTSCOUT_HOST"] + '/api/v1/entries.json?count=1')
    d=res1.json()
    pprint.pprint(d)
except:
    print "failed request entries"

try:
    entryid=d[0]['_id']
    glucose=d[0]['glucose']
    unfiltered=d[0]['unfiltered']
    filtered=d[0]['filtered']
    direction=d[0]['direction']
    noise=d[0]['noise']
    print 'entry id =',entryid,', direction=',direction,', noise=',noise
    print 'glucose =',glucose,', unfiltered=',unfiltered,', filtered=',filtered
except:
    print "Glucose not found in response to get entries"


try:
    res2 = requests.get(os.environ["NIGHTSCOUT_HOST"] + '/api/v1/devicestatus?count=1')      
    data2=res2.json()
    pprint.pprint(data2)
except:
    print "failed request devicestatus"


try:
    edison_battery=data2[0]['uploader']['battery']
    cob=data2[0]['openaps']['enacted']['COB']
    iob=data2[0]['openaps']['enacted']['IOB']
    tick=data2[0]['openaps']['enacted']['tick']
    enacttimestamp=data2[0]['openaps']['enacted']['timestamp']
    print 'enact timestamp =',enacttimestamp
    print 'tick =',tick
    print 'COB =',cob
    print 'IOB =',iob
    print 'edison battery =',edison_battery
except:
    print "Edison battery not found in response to get devicestatus"
    
test()

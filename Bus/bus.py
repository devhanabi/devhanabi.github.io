import json
import requests
import os
import time

url = "http://jaeryu.duckdns.org:3001/busroute?busid=1234"
posturl = "http://jaeryu.duckdns.org:3001/busgps"
geturl = "http://jaeryu.duckdns.org:3001/busbooking"

def sendGPS(ids,x, y):
    res = requests.post(posturl,
    data=json.dumps({"busid":ids,"busx":x, "busy" : y}),
     headers={'Content-Type': 'application/json'})
    print(ids, res)

def getGPS(ids,x , go):
    res = requests.get(geturl + "?busid=" + ids + " &stationid=" + x + "&go=" + go)
    print(res.json())
    if res.json()["result"]["data"] == "0":
        return False
    else:
        return True

if __name__ == "__main__":
    res = requests.get(url)
    maplist = res.json()["result"]["data"]["busroute"]
    maplist = sorted(maplist, key=lambda val: val['idx'])

    start = 0
    i = 0
    while True:
        if i == 50:
            start = (start + 1) % len(maplist)
            print(start)
            i = 0
            sendGPS("1234", int(maplist[start]['latitude']),  int(maplist[start]['longitude']))
            if(getGPS("1234", i, 0)):
                time.sleep(10)
                getGPS("1234", i, 1)
            else:
                time.sleep(3)
        else:
            x = int(int(maplist[(start + 1) % len(maplist)]['latitude']) - int(maplist[start]['latitude'])) // 50
            y = int(int(maplist[(start + 1) % len(maplist)]['longitude']) - int(maplist[start]['longitude'])) // 50
            i += 1
            sendGPS("1234", int(maplist[start]['latitude']) + x * i, int(maplist[start]['longitude']) + y * i)
            time.sleep(1)

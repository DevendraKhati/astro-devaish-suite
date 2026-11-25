#!/usr/bin/env python3
"""Optional VedAstro REST client. Falls back with a clear error if the host is unreachable
(e.g. sandboxes with a restricted network). Use jyotish.py for offline computation.
Usage: python vedastro_client.py HoroscopePredictions --input person.json [--ayanamsa RAMAN] [--key KEY]
       python vedastro_client.py MatchReport --a groom.json --b bride.json   (a=male, b=female)
       python vedastro_client.py NameNumberPrediction --name "Chandan Singh Bisht"
"""
import argparse, json, os, sys, urllib.request, urllib.parse
BASE="https://vedastro.zaishi.net/api/Calculate/"
def std(p):
    tz=p.get("tz",5.5); sign="+" if tz>=0 else "-"; h=int(abs(tz)); m=int(round((abs(tz)-h)*60))
    y,mo,d=p["dob"].split("-"); return {"StdTime":f"{p['tob']} {d}/{mo}/{y} {sign}{h:02d}:{m:02d}","Location":{"Name":p.get("place","Birth place"),"Longitude":p["lon"],"Latitude":p["lat"]}}
def call(method,body=None,key=None,get_suffix=""):
    h={"Content-Type":"application/json"}
    if key: h["x-api-key"]=key
    if body is None: req=urllib.request.Request(BASE+method+get_suffix,headers=h)
    else: req=urllib.request.Request(BASE+method,data=json.dumps(body).encode(),headers=h,method="POST")
    try:
        with urllib.request.urlopen(req,timeout=30) as r: return json.loads(r.read().decode())
    except Exception as e:
        return {"error":str(e),"hint":"Host unreachable or rate-limited (free tier = 5 calls/min). Use scripts/jyotish.py instead."}
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("method"); ap.add_argument("--input"); ap.add_argument("--a"); ap.add_argument("--b"); ap.add_argument("--name")
    ap.add_argument("--ayanamsa",default="RAMAN"); ap.add_argument("--key",default=os.environ.get("VEDASTRO_API_KEY"))
    a=ap.parse_args()
    if a.method=="NameNumberPrediction": r=call(a.method,None,a.key,"/Name/"+urllib.parse.quote(a.name))
    elif a.method=="MatchReport":
        r=call(a.method,{"MaleTime":std(json.load(open(a.a))),"FemaleTime":std(json.load(open(a.b))),"Ayanamsa":a.ayanamsa},a.key)
    else: r=call(a.method,{"Time":std(json.load(open(a.input))),"Ayanamsa":a.ayanamsa},a.key)
    print(json.dumps(r,indent=2))

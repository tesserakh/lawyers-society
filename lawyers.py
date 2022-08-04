import requests
import json
import time

url = "https://lawsocietyontario.search.windows.net/indexes/lsolpregistry/docs/search"
querystring = {"api-version":"2017-11-11"}
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "api-key": "212D535962D4563E62F8EC5D6E1C71CA",
    "Cache-Control": "no-cache",
    "Origin": "https://lso.ca",
    "Connection": "keep-alive",
    "Referer": "https://lso.ca/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Sec-GPC": "1",
    "TE": "trailers"
}

# total 81959 records

for n in range(0, 820):
  skip = n*100
  skip1 = (n+1)*100
  
  payload = {
    "search": "*",
    "count": True,
    "top": 100,
    "skip": skip,
    "orderby": "memberlastname, memberfirstname, membermiddlename",
    "queryType": "full"
  }
  
  response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
  
  time.sleep(3)
  
  filename = 'data/lawyers_'+str(skip+1)+'-'+str(skip1)+'.json'
  json_object = json.loads(response.text)['value']
  outfile = open(filename, "w")
  json.dump(json_object, outfile, indent = 4, sort_keys = False)
  outfile.close()


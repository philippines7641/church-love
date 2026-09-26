import json,os,urllib.parse,urllib.request
from pathlib import Path
API_KEY=os.environ["YOUTUBE_API_KEY"]
DB=Path("songs.json")
LIMIT=100
data=json.loads(DB.read_text(encoding="utf-8"))
songs=data["songs"]
def search(q):
 p=urllib.parse.urlencode({"part":"snippet","q":q,"type":"video","maxResults":5,"videoEmbeddable":"true","key":API_KEY})
 req=urllib.request.Request("https://www.googleapis.com/youtube/v3/search?"+p,headers={"User-Agent":"Church-Love-Bot/1.0"})
 with urllib.request.urlopen(req,timeout=20) as r:return json.load(r).get("items",[])
checked=added=0
for s in songs:
 if checked>=LIMIT: break
 if s.get("videoUrl"): continue
 checked+=1
 try: items=search(f'{s["category"]} {s["number"]}번')
 except Exception as e: print(e); break
 if items:
  item=items[0]; vid=item.get("id",{}).get("videoId")
  if vid:
   s["videoUrl"]=f"https://www.youtube.com/watch?v={vid}"
   s["foundVideoTitle"]=item.get("snippet",{}).get("title","")
   s["status"]="자동 등록"
   added+=1
DB.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
print("checked=",checked,"added=",added)

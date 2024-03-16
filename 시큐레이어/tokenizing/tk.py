import json 
import base64
from tknize import *

fname="test"
f = open(fname+".json")
output= open(fname+"_word.json","a")
jsons = json.load(f)

for payload in jsons:
	payload["DATA"] = DATA_word(payload["DATA"])
	payload["URI"] = URL_word(payload["URI"])
	payload["COOKIE"] = COOKIE_word(payload["COOKIE"])


output.write(json.dumps(jsons,ensure_ascii=False,indent=4))
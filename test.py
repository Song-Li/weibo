import json
import requests
import re

with open('try.html') as f:
    string = f.read()
    print string
    pattern = re.compile(r"<div class=..m_table_tit.. ><a href=....show.rid=(\w+)")
    for m in re.findall(pattern, string):
        print m

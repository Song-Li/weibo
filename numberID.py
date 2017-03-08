import json
import requests
import re
import codecs
import csv

features = [
    'id',
    'text',
    'source',
    'reposts_count',
    'comments_count',
    'attitudes_count',
    'isLongText',
    'pic_ids',
    'geo'
    ]
user_info = [
    'id',
    'screen_name',
    'verified',
    'verified_reason',
    'verified_type',
    'description',
    'gender',
    'followers_count',
    'follow_count',
    'mbtype',
    'urank',
    'mbrank',
    'statuses_count'
    ]

def getRepost(features, user_info, uid):
    url = 'http://m.weibo.cn/status/' + uid
    response = requests.get(url).content
    #print response
    pattern = re.compile(r"render_data = .(.+)..0.....\{\};", re.DOTALL)
    
    m = re.findall(pattern, response)[0]
    res = json.loads(m)
    #user = res['user']

    res = res['status']
    res_str = []
    for inx in features:
        addable = ""
        try:
            addable= str(res[inx])
        except:
            try:
                addable = res[inx]
            except:
                addable = 'None'

        addable = addable.encode('utf-8')
        res_str.append(addable)

    res = res['user']
    for inx in user_info:
        try:
            addable= str(res[inx])
        except:
            try:
                addable = res[inx]
            except:
                addable = 'None'

        addable = addable.encode('utf-8')
        res_str.append(addable)

    return res_str


f = open('IDall.txt', 'r')
fo = csv.writer(open('final.csv', 'a'))
title = features[:]
title.extend(user_info)
fo.writerow(title)
count = 0

for line in f:
    count += 1
    if len(line) < 3:
        continue;
    res_line = getRepost(features, user_info, line)
    fo.writerow(res_line)
    print count

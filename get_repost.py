import json
import requests

def getRepost(uid):
    num = 0
    for i in range(1, 1000):
        url = 'http://m.weibo.cn/api/statuses/repostTimeline?id=' + str(uid) + '&page=' + str(i)
        response = requests.get(url)
        res = response.json()
        if len(res['data']) == 0:
            break
        for inx in res['data']:
            print inx['user']['screen_name'],inx['user']['id'],inx['text'],inx['id']
            getRepost(inx['id'])
    return num

uid = input('Enter the Weibo id: ')
num = getRepost(uid)

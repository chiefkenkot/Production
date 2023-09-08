import requests
from datetime import datetime
import pandas as pd
import json

def fetch_glassnode(url,symbol,resolution,days=60,api_key=''):
    headers = {'x-api-key':api_key}

    params = {}
    params['url'] = url
    params['a'] = symbol
    params['i'] = resolution
    params['s'] = int(int(datetime.utcnow().timestamp()) - 60 * 60 * 24 * int(days))
    params['function'] = 'glassnode_requests'   # 指定需要的params

    res = requests.get(f"https://ewdtd9psag.execute-api.eu-west-2.amazonaws.com/API/glassnoderequest", params=params,headers=headers)
    return res

# 取近365天的數據
# fetch_glassnode(url="<API-Link>",symbol='<BTC/ETH/...>',resolution='<24h,1h,10m...>',days=<取得由開始至今多小天的數據>,api_key='<YOUR API-KEY>')
res = fetch_glassnode(url="https://api.glassnode.com/v1/metrics/addresses/active_count",
                      symbol='BTC',resolution='24h',days=365*1,api_key='qv0q4L1ExB4NjL4Lyy7zT2pbHOXdIMJ68VLC0R5m')

result = json.loads(res.text)
df = pd.DataFrame(json.loads(result['text']))
df['t'] = pd.to_datetime(df['t'],unit='s')
print(df)

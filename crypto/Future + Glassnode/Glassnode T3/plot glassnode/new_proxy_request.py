import requests
import json
import pandas as pd
from datetime import datetime

header={'x-api-key':'qv0q4L1ExB4NjL4Lyy7zT2pbHOXdIMJ68VLC0R5m'}
params = {
    'url':'https://api.glassnode.com/v1/metrics/addresses/active_count',
    'a':'ETH',
    'i':'24h',
    # 's':int(int(datetime.utcnow().timestamp()) - 60 * 60 * 24 * 365*5),  # 此param 需要設 'mode':'backtest', 才會有效
    # 'mode':'backtest',  # 使用這個param 可解除扲數據的長度限制, 因他不會把你拿取的data 放進proxy cache內, 如不使用此param,會無視你設定param s, proxy 只會return 近1年內的數據
}

base_url = 'http://13.41.191.61/glassnode'

res = requests.get(base_url, headers=header, params=params)
json_format = json.loads(res.text)
df = pd.DataFrame(json.loads(json_format['text']))
df['t'] = pd.to_datetime(df['t'], unit='s') # 把unixtime 時間轉換到人睇的時間
print(df)



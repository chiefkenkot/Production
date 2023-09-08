import concurrent.futures
import time
import requests
from datetime import datetime,timedelta,timezone
from socondary_y import secondary_yaxis
import orjson as json
import pandas as pd

defalt_datetime_str = None
API='qv0q4L1ExB4NjL4Lyy7zT2pbHOXdIMJ68VLC0R5m'


def fetch_glassnode(
        url,                                # API LINK
        symbol,                             # Asset
        resolution,                         # 10m 1h 24h
        days=365,                            # 取近幾多日的數據
        api_key=API,                        # your AWS API　ＫＥＹ
        defalt_datetime_str='date',         # 預設timestamp column 的名稱 （可隨意更改）
        defalt_value_str='close_value',     # 預設value column 的名稱 （可隨意更改）
        each_size = 365*1,                  # 如數據長度大於該值（each_size），程式會自動分開每隔 X day(each_size) 去ｒｅｑｕｅｓｔ一次
        **kwargs):                          #
    def request(**kwargs):
        while True:
            base_url = 'https://ewdtd9psag.execute-api.eu-west-2.amazonaws.com/API/glassnoderequest'
            res = requests.get(base_url, params=kwargs.get('params'), headers=kwargs.get('headers'))
            if res.status_code == 200:
                print('Rate-Limit-Remaining: ',json.loads(res.text)['Rate-Limit-Remaining'])
                break
            else:
                print(f'status_code:{res.status_code}, reason: {res.reason}, we will request again. {str(datetime.utcnow() + timedelta(hours=8))[0:19]}')
                time.sleep((5))
        return res
    globals()['defalt_datetime_str'] = defalt_datetime_str
    cond10m = resolution == '10m'
    cond1h = resolution == '1h'
    condover365_1 = days > each_size
    condover365_2 = (datetime.utcnow() - datetime.fromtimestamp(kwargs.get('s',datetime.utcnow().timestamp()))).days > each_size
    results = []
    headers = {'x-api-key':api_key}
    if cond1h or cond10m and (condover365_1 or condover365_2):
        pool_var_list = []
        params = {}
        if kwargs.get('s') == None:
            params['s'] = int(((datetime.utcnow() - timedelta(days=days)).astimezone(timezone.utc)).timestamp())
        else:
            params['s'] = kwargs.get('s')
        params['u'] = int((datetime.fromtimestamp(params['s']) + timedelta(days=each_size)).astimezone(timezone.utc).timestamp())
        while True:
            params['url'] = url
            params['a'] = symbol
            params['i'] = resolution
            params['function'] = 'glassnode_requests'
            pool_var_list.append(params.copy())
            params['s'] = params['u']
            params['u'] = int((datetime.fromtimestamp(params['s']) + timedelta(days=each_size)).astimezone(timezone.utc).timestamp())
            if params['u'] > datetime.utcnow().timestamp():
                del params['u']
                pool_var_list.append(params.copy())
                break
        # 創建一個 ThreadPoolExecutor 對象，設置線程池的大小
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            # 向線程池提交任務
            futures = [executor.submit(request, params=i,headers=headers) for i in pool_var_list]
            # 等待所有任務完成並獲取結果
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
            # 輸出結果
    else:
        params = {}
        params['url'] = url
        params['a'] = symbol
        params['i'] = resolution
        if kwargs.get('s') == None:
            params['s'] = int(int(datetime.utcnow().timestamp()) - 60 * 60 * 24 * days)
        else:
            params['s'] = kwargs.get('s')
        params['function'] = 'glassnode_requests'

        results = [request(params=params,headers=headers)]


    all_df = pd.DataFrame()
    for i in results:
        result = json.loads(i.text)
        df = pd.DataFrame(json.loads(result['text']))
        if not df.empty:
            if 'o' in list(df.columns):
                o_df = pd.json_normalize(df['o'])
                df = pd.merge(df,o_df,left_index=True,right_index=True)
                df.drop('o', axis=1, inplace=True)
            df.rename(columns={'t':defalt_datetime_str,'v':defalt_value_str},inplace=True)
            all_df = all_df.append(df,ignore_index=True)
    if not all_df.empty:
        all_df[defalt_datetime_str] = pd.to_datetime(all_df[defalt_datetime_str], unit='s')
        all_df.drop_duplicates(subset=defalt_datetime_str,inplace=True)
        all_df.sort_values(by=defalt_datetime_str, inplace=True)
        all_df[defalt_datetime_str] = all_df[defalt_datetime_str].apply(lambda x:str(x)[0:19])
        all_df = all_df.reset_index().drop('index', axis=1)
        return all_df
    else:
        return 'Empty dataframe'

if __name__ == '__main__':
    url = 'https://api.glassnode.com/v1/metrics/supply/active_1d_1w'

    days = (datetime.utcnow() - datetime(2020,1,1)).days
    resolution='24h'
    symbol = 'BTC'

    df = fetch_glassnode(url=url, symbol=symbol,resolution=resolution, days=days)
    ohlc_df = fetch_glassnode(url='https://api.glassnode.com/v1/metrics/market/price_usd_close', symbol=symbol,resolution=resolution, days=days,defalt_value_str='close')

    print('df columns list',list(df.columns))
    factor_list = list(df.filter(regex=fr'\b(?!{defalt_datetime_str}\b)\S+\b[ !]?').columns)
    secondary_yaxis(df,ohlc_df['date'],ohlc_df['close'],df[defalt_datetime_str],df[factor_list],main_title=f"{url.split('/')[-2]}_{url.split('/')[-1]}")
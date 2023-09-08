import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import requests,time,datetime,json,logging
import plotly.graph_objects as go
from plotly.subplots import make_subplots
log = logging.getLogger()

pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
pd.set_option('display.width',1000)

api_key = 'qv0q4L1ExB4NjL4Lyy7zT2pbHOXdIMJ68VLC0R5m'   ######### your api key ###########

def fetch_glassnode(url,api_key,symbol,since,resolution,ex=None,force_request=None):
    params = {}
    headers = {'x-api-key':api_key}
    params['url'] = url
    params['a'] = symbol
    params['i'] = resolution
    params['e'] = ex
    params['s'] = since
    params['force_request'] = force_request
    params['function'] = 'glassnode_requests'
    res = requests.get(f"https://ewdtd9psag.execute-api.eu-west-2.amazonaws.com/API/glassnoderequest",headers=headers, params=params)
    data = json.loads(res.json()['text'])
    df = pd.DataFrame(data)
    df['t'] = df['t'].map(lambda x: datetime.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    return df

def glassnode_plot_chart(url,value_sym,price_sym,resolution,factor:list,value_col='o',since=None,ex=None,force_request=None):
    df_value = fetch_glassnode(url,api_key,value_sym,since,resolution,ex=ex,force_request=force_request)
    df_price = fetch_glassnode('https://api.glassnode.com/v1/metrics/market/price_usd_close',api_key,price_sym,since,resolution,ex=ex,force_request=force_request)
    df = pd.merge(df_value,df_price,on='t',how='inner')
    if 'v_x' and 'v_y' in df.columns:
        df.rename(columns={'v_x': 'value', 'v_y': 'price'}, inplace=True)
    else:
        df.rename(columns={value_col: 'value', 'v': 'price'}, inplace=True)
    value_title = url.split('/')[-1]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    try:
        if type(df['value'].values[0]) == dict:
            raise Exception('please add factors')
        fig.add_trace(go.Scatter(x=df['t'], y=df['value'], name=f'{value_title}'))

    except:
        for i in factor:
            factors = df['value'].map(lambda x:x.get(i))
            fig.add_trace(go.Scatter(x=df['t'], y=factors,name=f'{value_title}_{i}'))

    fig.add_trace(go.Scatter(x=df['t'], y=df['price'],name=f'{price_sym}_price',line=dict(color='black')),secondary_y=True)

    fig.update_layout(title=value_title,xaxis_title='t',yaxis_title='value',yaxis2_title=f'{price_sym}_price',)

    return fig.show()


url = 'https://api.glassnode.com/v1/metrics/derivatives/options_25delta_skew_all'     ##### glassnode endpoints link ########
value_underlying = 'BTC'
price_underlying = 'BTC'
resolution = '24h'   ########## 24h,1h,10m #########
start = 0     ######### unix time #############
# sub_factor=None
factor = ['1w','1m','3m']
glassnode_plot_chart(url,value_underlying,price_underlying,resolution,since=start,factor=factor)
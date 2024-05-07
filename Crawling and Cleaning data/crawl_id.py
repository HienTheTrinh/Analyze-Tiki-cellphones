# sourcery skip: remove-duplicate-dict-key
import requests
import time
import random
import pandas as pd
#from tqdm import tqdm

# Find page of product we want to crawl data -> get id
# Click first product -> get info and comments

# Click "Inspect" -> "Network" and reload the page.
# Find thing that contains "data" that we need
# Click "Preview" to see data
# Click "Payload" to find params
# Click "Headers" to find cookies and header

cookies = {
    '_trackity':'10f7cca8-b77b-3e7b-0e29-dd7bba8c6474', 
    '_gcl_au':'1.1.1400552038.1687945122', 
    '_fbp':'fb.1.1687945122680.1806540917', 
    '__uidac':'d42c930931cfc13bae15ee2d1288983b', 
    '_ga_HK3PZ9B06G':'GS1.1.1693943831.1.1.1693943863.0.0.0', 
    '_ga_KNZCHDVZCP':'GS1.1.1693943868.1.1.1693943920.0.0.0', 
    'TOKENS':'{%22access_token%22:%22IHCgvqly2bWKZcNmEBV6ewx8DXruO3a0%22}',
    '_hjSessionUser_522327':'eyJpZCI6ImMwODUwZDhiLTUxMjAtNTQxNy04MTc0LWYzNjYwOTVlOTMwMyIsImNyZWF0ZWQiOjE2ODc5NDUxMjI3ODEsImV4aXN0aW5nIjp0cnVlfQ==', 
    '__iid':'749', 
    '__iid':'749', 
    '__su':'0', 
    '__su':'0', 
    '_ga_W6PZ1YEX5L':'GS1.1.1694023534.1.1.1694023545.0.0.0',
    'TKSESSID':'fc71aeee3724eaad03fbf2a958839b0b', 
    'tiki_client_id':'1112102684.1687945119', 
    '_gid':'GA1.2.1922180357.1694754936',
    'delivery_zone':'Vk4wMzkwMjMwMTE=',
    '_hjIncludedInSessionSample_522327':'0', 
    '_hjSession_522327':'eyJpZCI6ImQ0MmQ3MGI1LTAzOGEtNGNjZC05ZjEyLWJjMDdhZTBhMmIyMCIsImNyZWF0ZWQiOjE2OTQ3NTQ5NDA5MDAsImluU2FtcGxlIjpmYWxzZX0=', 
    'dtdz':'e6be8c59-7da9-4191-9038-e7d66ed0b4e5',
    'amp_99d374':'JxlTv-OuxZclBlFvtjPQYK...1habk7v1k.1habkjuma.n8.tr.1l3', 
    '_gat':'1',
    '_ga_GSD4ETCY1D':'GS1.1.1694754938.18.1.1694755324.37.0.0', 
    '_ga':'GA1.1.1112102684.1687945119'
}

headers_id = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Avast/116.0.0.0',
    'Accept':'application/json, text/plain, */*',
    'Accept-Language':'en-US,en;q=0.9',
    'Referer':'https://tiki.vn/dien-thoai-may-tinh-bang/c1789',
    'X-Guest-Token':'IHCgvqly2bWKZcNmEBV6ewx8DXruO3a0'
}

params_id = {
    'limit': '40',
    'include': 'advertisement',
    'aggregations': '2',
    'version': 'home-persionalized',
    'trackity_id': '10f7cca8-b77b-3e7b-0e29-dd7bba8c6474',
    'category': '1789',
    'page': '1',
    'urlKey': 'dien-thoai-may-tinh-bang',
}

# Part 1: Get product's id
product_id = []
'''for i in range(1,11):
    params_id['page']=i
    response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', 
                            headers=headers_id, params=params_id)
    if response.status_code==200:
        print('Request id success!')
        product_id.extend(
            {'id': record.get('id')} for record in response.json().get('data')
        )
    time.sleep(random.randrange(3,10))'''

i=1
while (True):    # Crawl all
    params_id['page']=i
    response = requests.get('https://tiki.vn/api/personalish/v1/blocks/listings', 
                            headers=headers_id, params=params_id, cookies=cookies)
    if response.status_code==200:
        print('Request id success!')
        product_id.extend(
            {'id': record.get('id')} for record in response.json().get('data')
        )       
    else:
        print('Fail!!')
        break
    time.sleep(random.randrange(3,10))
    i+=1

data_id = pd.DataFrame(product_id)
data_id.to_csv('data/id.csv', index=False)
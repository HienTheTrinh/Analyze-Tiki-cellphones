# sourcery skip: remove-duplicate-dict-key
import requests
import time
import random
import pandas as pd
from tqdm import tqdm

product_id = '205750556'
referer = "https://tiki.vn/dien-thoai-oppo-a57-4gb-128gb-hang-chinh-hang-p205750556.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.273278_Y.1855598_Z.3858365_CN.AUTO---%C4%90ien-Thoai-Oppo-A57-4GB%2F128GB---Hang-Chinh-Hang---2023%2F09%2F25-10%3A40%3A01&itm_medium=CPC&itm_source=tiki-ads&spid=263117365"

# Part 3: Get comments
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
    'dtdz':'e6be8c59-7da9-4191-9038-e7d66ed0b4e5', 
    '_ga':'GA1.1.1112102684.1687945119', 
    'amp_99d374':'JxlTv-OuxZclBlFvtjPQYK...1habnc09s.1habnc0nh.nf.u4.1lj',
    '_ga_GSD4ETCY1D':'GS1.1.1694758209.19.0.1694758209.60.0.0'
}

headers_comments = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Avast/116.0.0.0',
    'Accept':'application/json, text/plain, */*',
    'Accept-Language':'en-US,en;q=0.9',
    'Referer':referer,
    'X-Guest-Token':'IHCgvqly2bWKZcNmEBV6ewx8DXruO3a0'
}

params_comments = {
    'limit': '5',
    'include': 'comments',
    'sort': 'score|desc,id|desc,stars|all',
    'page': 1,
    'product_id': product_id
}

def parse_comment(json_file):
    p = {'product_id': json_file.get('product_id')}
    p['customer_id']  = json_file.get('customer_id')
    #p['customer_name'] = json_file.get('created_by').get('name')
    try:
        p['customer_region'] = json_file.get('created_by').get('region')
    except Exception:
        p['customer_region'] = 'Unknown'
    p['customer_evaluate'] = json_file.get('title')

    p['content'] = json_file.get('content')
    p['like_count'] = json_file.get('thank_count')
    p['rating'] = json_file.get('rating')
    try:
        p['score'] = json_file.get('score')
    except Exception:
        p['score'] = 'Unknown'
    p['created_at'] = json_file.get('created_at')
    #p['review_created_date'] = json_file.get('timeline').get('review_created_date')
    #p['purchased_at'] = json_file.get('created_by').get('purchased_at')
    return p

def get_star(json_file, p):
    p['rating_1_stars'] = json_file.get('1').get('count')
    p['rating_2_stars'] = json_file.get('2').get('count')
    p['rating_3_stars'] = json_file.get('3').get('count')
    p['rating_4_stars'] = json_file.get('4').get('count')
    p['rating_5_stars'] = json_file.get('5').get('count')
    return p

id_df = pd.read_csv('data/id.csv').id.to_list()
result = []
p = {}
for pid in tqdm(id_df, total=len(id_df)):
    params_comments['product_id'] = pid
    print(f'Crawl comment for product {pid}')
    '''try:
        page = requests.get('https://tiki.vn/api/v2/reviews', headers=headers_comments, params=params_comments, cookies=cookies).json().get('paging').get('last_page')
    except Exception:
        page = 0
        continue'''
    # Too many request -> server refuse
    for i in range(1,2+1):        #3
        params_comments['page'] = i
        response = requests.get('https://tiki.vn/api/v2/reviews', 
                                headers=headers_comments, params=params_comments, cookies=cookies)
        if response.status_code == 200:
            print(f' Crawl comment page {i} success!!!')
            for comment in response.json().get('data'):
                p = parse_comment(comment)
                result.append(get_star(response.json().get('stars'), p))
        #time.sleep(random.randrange(3,10))
    #time.sleep(random.randrange(3,10))

data_comment = pd.DataFrame(result)
data_comment.to_csv('data/comments.csv', index=False)

# sourcery skip: remove-duplicate-dict-key
import requests
import time
import random
import pandas as pd
from tqdm import tqdm

# Find page of product we want to crawl data -> get id
# Click first product -> get info and comments

# Click "Inspect" -> "Network" -> "Fetch/XHR" and reload the page
# Find thing that contains "data" that we need
# Click "Preview" to see data
# Click "Payload" to find params
# Click "Headers" to find cookies and header

# Info of 1st product in page
spid = 263117365
referer = "https://tiki.vn/dien-thoai-oppo-a57-4gb-128gb-hang-chinh-hang-p205750556.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.273278_Y.1855598_Z.3858365_CN.AUTO---%C4%90ien-Thoai-Oppo-A57-4GB%2F128GB---Hang-Chinh-Hang---2023%2F09%2F25-10%3A40%3A01&itm_medium=CPC&itm_source=tiki-ads&spid=263117365"
x_guest_token = 'IHCgvqly2bWKZcNmEBV6ewx8DXruO3a0'

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

# Part 2: Through id, get product's info
headers_product = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Avast/116.0.0.0',
    'Accept':'application/json, text/plain, */*',
    'Accept-Language':'en-US,en;q=0.9',
    'Referer':referer,
    'X-Guest-Token':x_guest_token
}

params_product = (
    ('platform', 'web'),
    ('spid', spid),
    ('version', 3)
    #('include', 'tag,images,gallery,promotions,badges,stock_item,variants,product_links,discount_tag,ranks,breadcrumbs,top_features,cta_desktop'),
)

def parse_product(json_file):
    p = {'product_id': json_file.get('id')}
    if json_file.get('inventory_status') == 'available':
        p['sku'] = json_file.get('sku')
        p['product_name'] = json_file.get('name')
        p['brand_name'] = json_file.get('brand').get('name')
        p['categories'] = json_file.get('categories').get('name')
        p['current_seller'] = json_file.get('current_seller').get('name')

        try:
            p['warranty_time'] = json_file.get('warranty_info')[0].get('value')
        except Exception:
            p['warranty_time'] = 'Unknown'

        try:
            p['quantity_sold'] = json_file.get('quantity_sold').get('value')
        except Exception:
            p['quantity_sold'] = 0

        p['rating_average'] = json_file.get('rating_average')
        p['review_count'] = json_file.get('review_count')

        p['price'] = json_file.get('price')
        p['original_price'] = json_file.get('original_price')
        p['discount'] = json_file.get('discount')
        p['discount_rate'] = json_file.get('discount_rate')

        #p['list_price'] = json_file.get('list_price')
        p['stock_item_qty'] = json_file.get('stock_item').get('qty')
        p['stock_item_max_sale_qty'] = json_file.get('stock_item').get('max_sale_qty')

        p['short_description'] = json_file.get('short_description')
        p['link'] = f"https://tiki.vn/{json_file.get('url_path')}"
        
    return p

id_df = pd.read_csv('data/id.csv').id.to_list()
result = [] 
for pid in tqdm(id_df, total=len(id_df)):
    response_product = requests.get(f'https://tiki.vn/api/v2/products/{pid}', 
                                    headers=headers_product, params=params_product)
    if response_product.status_code==200:
        print(f' Start to crawl with id {pid}')
        result.append(parse_product(response_product.json()))
    else:
        print('Fail!')
        break
    print('Success!!')
    time.sleep(random.randrange(3,11))

data_product = pd.DataFrame(result)
data_product.to_csv('data/product.csv', index=False)
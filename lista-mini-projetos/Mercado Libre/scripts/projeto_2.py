# Imports
import requests
import pandas as pd
import functools as a
import csv

item_range = 10
items = ['chromecast', 'Google Home', 'Apple TV', 'Amazon Fire TV']

features = ['site_id', 'title', 'subtitle', 'seller_id', 'category_id', 'official_store_id', 'price', 'base_price'
            , 'original_price', 'currency_id' 'initial_quantity', 'available_quantity', 'sold_quantity', 'sale_terms',
               'buying_mode']

result_csv_file = '\projetos\mercado_libre_items_output.csv'

# Função que varre os itens e retorna suas respectivas informações
def get_info(item):
    return [requests.get(f"https://api.mercadolibre.com/sites/MLA/search?q={item}&limit={item_range}&offset={num}").json()
            for num in range(1, item_range+1)]

# Obtém as informações do item com base no Item_id.
def get_item_info(item_id):
    url = f"https://api.mercadolibre.com/items/{item_id}"
    response = requests.get(url)

    if response.status_code == 200:
        item_info = response.json()
        return item_info
    else:
        return None

# result_list contém os dicionários de informações para cada combinação de item e número de página
result_list = a.reduce(lambda result, item: result + get_info(item), items, [])

# 
items_mercado_libre = [get_item_info(result['id']) for result in result_list[0]['results']]


# 
with open(result_csv_file, 'w', newline='', encoding='utf-8') as result_file:
    writer = csv.writer(result_file)
    
    writer.writerow(features)
    
    for item in items_mercado_libre:
        row = []
        
        for feature in features:
            if feature in item:
                row.append(item[feature])
            else:
                row.append('')
        writer.writerow(row)
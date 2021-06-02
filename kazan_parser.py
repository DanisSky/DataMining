# -*- coding: utf-8 -*-
"""kazan_parser.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1It_n8_a3gte2KHVZF6U5SOCaWnNnZ-1h
"""
import requests
import csv
import pandas as pd
from collections import defaultdict


volga_federal_district_url = 'https://download.geofabrik.de/russia/volga-fed-district-latest.osm.bz2'

def download_file(url):
    local_filename = '/content/drive/MyDrive/DataMiningPractice/' + url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
   
    return local_filename

file_name = download_file(volga_federal_district_url)
file_name


file = open('/content/drive/MyDrive/DataMiningPractice/kazan_map','r',encoding='utf-8').read()
soup = BeautifulSoup(file,'xml')

"""Координаты всех светофоров"""

with open('/content/drive/MyDrive/DataMiningPractice/traffic_signals.csv', 'w') as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerow(["id", "lat", "lon"])
    for node in soup.findAll('node'):
        for tag in node.findAll('tag'):
            if tag['v'] == 'traffic_signals':
                writer.writerow([node['id'], node['lat'], node['lon']])

"""Координаты всех остановок"""

with open('/content/drive/MyDrive/DataMiningPractice/bus_stops.csv', 'w') as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerow(["id", "lat", "lon", "bus_stop_name", "bus"])
    for node in soup.findAll('node'):
        is_bus_stop = False
        for tag in node.findAll('tag'):
            if tag['v'] == 'bus_stop':
                is_bus_stop = True
        if is_bus_stop:
            try :
                name = node.find('tag', k='name')['v']
            except TypeError:
                name = None
            try :
                is_bus = node.find('tag', k='bus')['v']
            except TypeError:
                is_bus = None
            writer.writerow([node['id'], node['lat'], node['lon'], name, is_bus])

"""Все данные точек с тегами"""

columns = defaultdict(int)
nodes_count = len(soup.findAll('node'))
for node in soup.findAll('node'):
    for k,v in node.attrs.items():
        columns[k] += 1
        for tag in node.findAll('tag'):
            for k,v in tag.attrs.items():
                columns[v] += 1
                break
columns = sorted(columns.items(), key=lambda t: t[1], reverse=True)

columns_to_add = []
for k, v in columns:
    if v > 6000:
        columns_to_add.append(k)
columns_to_add

df = pd.DataFrame(columns=columns_to_add)
for node in tqdm(soup.findAll('node')):
    row = {}
    for k, v in node.attrs.items():
        if k in df.columns:
            row[k] = v 
    for tag in node.findAll('tag'):
        attrs = list(tag.attrs.values())
        if attrs[0] in df.columns:
            row[attrs[0]] = attrs[1]
    df = df.append(row, ignore_index=True)
df.head()

df.to_excel('/content/drive/MyDrive/DataMiningPractice/data.xlsx',sheet_name='data')

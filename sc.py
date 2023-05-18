import requests
import json
import pandas as pd
import boto3
import matplotlib.pyplot as plt
import csv
import io

url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'

#task1
response = requests.get(url)
text = response.json()
jsonstr = json.dumps(text, ensure_ascii=False)

#task2
df = pd.read_json(jsonstr)
df.to_csv('file.csv')

#task3
s3 = boto3.client('s3')
with open("file.csv", "rb") as f:
    s3.upload_fileobj(f, "senpainfjbucket", "newfile.csv")

#task4
obj = s3.get_object(
    Bucket = 'senpainfjbucket',
    Key = 'newfile.csv'
)
data = pd.read_csv(obj['Body'])
data = data.drop(labels=range(57, 61), axis=0)

data.plot.bar(x='cc', y='rate', figsize = (15, 5), xlabel='Currency')

img_data = io.BytesIO()
plt.savefig(img_data, format='png')
img_data.seek(0)


s3.upload_fileobj(img_data, "senpainfjbucket", "1.png")
plt.close()

#task5
urlusd = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=usd&sort=exchangedate&order=asc&json"
urleur = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode=eur&sort=exchangedate&order=asc&json"

response = requests.get(urlusd)
text = response.json()
jsonstr = json.dumps(text, ensure_ascii=False)
df = pd.read_json(jsonstr)

response = requests.get(urleur)
text = response.json()
jsonstr = json.dumps(text, ensure_ascii=False)
df2 = pd.read_json(jsonstr)

ax = df.plot(x='exchangedate', y='rate', label ='USD')
df2.plot(ax=ax, x='exchangedate', y='rate', label ='EUR', figsize = (15, 5), xlabel='Time')

img_data1 = io.BytesIO()
plt.savefig(img_data1, format='png')
img_data1.seek(0)

s3.upload_fileobj(img_data1, "senpainfjbucket", "2.png")
plt.close()


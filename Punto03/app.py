from dataclasses import replace
from genericpath import exists
from itertools import count
from multiprocessing import cpu_count
from queue import Empty
import boto3
import json
import pandas as pd
import html_to_json
import requests
import urllib.request
from bs4 import BeautifulSoup
from datetime import date


def app(event, context):

    today = date.today()
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)
    # page = requests.get('https://www.bbc.com/')
    # soup_1 = BeautifulSoup(page.text, 'html.parser')
    directory_periodic = "periodico=bbc/year=" + \
        year+"/month="+month+"/day="+day
    # directory_search_bbc = "/headlines/raw/Periodico=bbc/year="+year+"/month="+month+"/day="+day+"/bbc.html"
    s3 = boto3.resource('s3')
    obj = s3.Object(
        'proyecto02', 'headlines/raw/periodico=bbc/year=2022/month=4/day=24/2022_4_24_23_30_bbc.html')
    # j=obj.get()['Body'].read().decode('utf-8')
    # s3 = boto3.resource('s3')
    # content_object = s3.Object('bcc2', directory_search_bbc)
    file_content = obj.get()['Body'].read()
    soup = BeautifulSoup(file_content, 'html.parser')
    section_items = soup.find_all('h3')
    category = ""
    alfa1 = ""
    alfa2 = ""
    alfa3 = ""
    # print(section_items[0])
    # print(section_items[0].find("a").get_text())
    # print(section_items[0].find("a")["href"])
    # ss = section_items[0].find("a")["href"].split("/")
    # print(ss)
    # print(ss[2][:12])

    for i in range(len(section_items)):
        # category.append(i_sect.find(class_='media__tag tag tag--new'))
        # alfa1 = str(i_sect.get_text()).strip()
        # alfa2 = str(i_sect.get_text()).strip()
        # alfa3 = str(i_sect.get_text()).strip()
        if str(section_items[i].get_text()) != "None":
            alfa1 = str(section_items[i].get_text().strip())
            if section_items[i].find("a") is not None:
                # print(section_items[i].find("a"))s
                ss = section_items[i].find("a")["href"].split("/")
                alfa2 = ss[2][:12]
                alfa3 = section_items[i].find("a")["href"]

                category += "Title: " + alfa1 + ", "
                category += "Category: " + alfa2 + ", "
                category += "Link: "+alfa3 + "\n"

    category = category.replace("\t", "")
    category = category.replace("  ", "")
    category = category.split("\n")
    df = pd.DataFrame(category)
    csv = df.to_csv(index=False)
    s3Object_1 = s3.Object('proyecto02punto03', directory_periodic+'/bbc.csv')
    s3Object_1.put(Body=csv)


# app(None, None)

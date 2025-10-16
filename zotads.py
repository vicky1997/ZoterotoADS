import numpy as np
import requests
import json
from pyzotero import zotero
from urllib.parse import urlencode
import pandas as pd

class zot:
    def __init__(self):
        self.library_id = ''
        self.library_type = 'user'
        self.api_key = ''
        self.collection_id = ''
    def getlib(self, lib_id='', lib_type='user', api_key=''):
        self.library_id = lib_id
        self.library_type = lib_type
        self.api_key = api_key
        if(len(self.library_id) < 1 and len(self.api_key) < 1):
            raise ValueError('library ID and api_key are empty strings')
        self.zotlib = zotero.Zotero(self.library_id,self.library_type,self.api_key)       
    def getcollection(self, collection_id=''):
        self.collection_id = collection_id
        if(len(self.collection_id) < 1):
            raise ValueError('collection ID is an empty string')
        self.collection_items = self.zotlib.collection_items(self.collection_id)
        self.df = pd.DataFrame.from_dict(self.collection_items)
        #print(self.collection_items.json())
class adslib:
    def __init__(self):
        self.token = ''
        self.api = 'https://api.adsabs.harvard.edu/v1/'
    def gettoken(self,token=''):
        self.token = token


def generatebibtex(zots,adslib,filename='bibliography.bib'):
    dois = []
    titles = []
    i=0
    for item in zots.collection_items:
        print('item: %s | Key: %s' %(item['data']['itemType'], item['data']['title']))
    for item in zots.collection_items:
        if(item['data']['itemType']== 'journalArticle'):
            i=i+1
            print(item['data']['DOI'])
            if(item['data']['DOI']==''):
                print("DOI is empty in %s"%(item['data']['title']))
            else:
                dois.append(item['data']['DOI'])
                titles.append(item['data']['title'])
    bibcodes = []
    for doidoi,title in zip(dois,titles):
        encoded_query = urlencode({"q": "doi:"+doidoi,
                               "fq": "database:astronomy",
                               "fl": "bibcode,title"})
        results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                           headers={'Authorization': 'Bearer ' + adslib.token})
        resultsjson = results.json()
        try:
            bibcodes.append(resultsjson['response']['docs'][0])
        except:
            print("Error in parsing bibcode, trying with title of the paper")
            encoded_query = urlencode({"q": title ,
                               "fq": "database:astronomy",
                               "fl": "bibcode,title"})
            results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                           headers={'Authorization': 'Bearer ' + adslib.token})
            resultsjson = results.json()
            try:
                bibcodes.append(resultsjson['response']['docs'][0])
                #print('parsing with titles worked, one final check')
                if(title==resultsjson['response']['docs'][0]['title'][0]):
                    print("all good, title worked")
                else:
                    print("title mismatch")
                    print("Zotero:",title)
                    print("ADS:",resultsjson['response']['docs'][0]['title'][0])
            except:
                print(resultsjson['error'])
                print('error parsing title')
    for bibs in bibcodes:
        results = requests.get("https://api.adsabs.harvard.edu/v1/export/bibtex/"+bibs['bibcode'], \
                           headers={'Authorization': 'Bearer ' + adslib.token})
        resultstext=results.text
        with open(filename, "a+") as file:
            file.write(resultstext)

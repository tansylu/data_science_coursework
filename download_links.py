import os, sys, glob, re
import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs,SoupStrainer
import pandas as pd
import numpy as np
import uuid
import time

from config import LINK_LIST_PATH, BASE, ROOT

# Encoding for writing the URLs to the .txt file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"


def save_link(url, page):
    """
    Save collected link/url and page to the .txt file in LINK_LIST_PATH
    """
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, url).hex
    with open(LINK_LIST_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, url, str(page)]) + "\n")


def download_links_from_index():

    """
    This function should go to the defined "url" and download the news page links from all
    pages and save them into a .txt file.
    """
    downloaded_url_list = []
    collected_url = ""

    # Checking if the link_list.txt file exists
    if not os.path.exists(LINK_LIST_PATH):
        with open(LINK_LIST_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "url", "page"]) + "\n")
        start_page = 1
        downloaded_url_list = []

    # If some links have already been downloaded,
    # get the downloaded links and start page
    else:
        # Get the page to start from
        data = pd.read_csv(LINK_LIST_PATH, sep="\t")
        if data.shape[0] == 0:
            start_page = 1
            downloaded_url_list = []
        else:
            start_page = data["page"].astype("int").max()
            downloaded_url_list = data["url"].to_list()

    # WRITE YOUR CODE HERE
    #########################################
    # Start downloading from the page "start_page"
    # which is the page you ended at the last
    # time you ran the code (if you had an error and the code stopped)
    #"https://www.gob.mx/sre/en/archivo/prensa"
    #https://www.gob.mx/sre/en/archivo/prensa?idiom=en&order=DESC&page=301
    # Save the collected url in the variable "collected_url"
    #goes until page 301

    for i in range(1, 301):

        r =  requests.get(f'{BASE}{i}')
        print(r.status_code)
        print(f'{BASE}{i}')
        b =  bs(r.content,  'lxml')
        all_links = b.find_all('a', href=True)
        print(len(all_links))
        count = 0
        for link in all_links:
           
            collected_url = link.get('href')
            print(collected_url)
            if "page" not in collected_url:
                count +=1
                print(f"page:{i} link no:{count}")

                # Save the page that the url is taken from in the variable "page"
                page = i

                # The following code block saves the collected url and page
                # Save the collected urls one by one so that if an error occurs
                # you do not have to start all over again
                if collected_url not in downloaded_url_list:
                    print("\t", collected_url, flush=True)
                    save_link(collected_url, page)
            
        time.sleep(4)
#########################################
if __name__ == "__main__":
    download_links_from_index()

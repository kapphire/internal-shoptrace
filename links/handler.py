from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re
import json

def hail_mary(soup):
    try:
        s = str(soup)
        qty = re.search('(?<=inventory_quantity":)(.*?)(?=\,)', s).group(0)
        identity = re.search('(?<=id":)(.*?)(?=\,)', s).group(0)
        vendor = re.search('(?<=vendor":)(.*?)(?=\,)'.replace("\v", "v"), s).group(0)
        name = re.search('(?<=name":)(.*?)(?=\,)'.replace("\n", "n"), s).group(0)

        product = {
            "name": name.replace('"', ''),
            "id": identity,
            "vendor": str(re.sub('[^A-Za-z0-9]+', '', vendor)).lower(),
        }
    except AttributeError:
        return dict()
    return product


def parse_product(link):
    products = list()
    resp = requests.get(link, verify=False).text
    soup = BeautifulSoup(resp, "html.parser")
    # Firstly Find Products from Scripts
    scripts = soup.findAll("script")
    for script in scripts:
        try:
            if not "inventory_quantity" in script.text:
                continue

            qty = re.search('(?<=inventory_quantity":)(.*?)(?=\,)', script.text).group(0)
            identity = re.search('(?<=id":)(.*?)(?=\,)', script.text).group(0)
            vendor = re.search('(?<=vendor":)(.*?)(?=\,)'.replace("\v", "v"), script.text).group(0)
            name = re.search('(?<=name":)(.*?)(?=\,)'.replace("\n", "n"), script.text).group(0)

            product = {
                "name": name.replace('"', ''),
                "identity": identity,
                "quantity": qty,
                "vendor": str(re.sub('[^A-Za-z0-9]+', '', vendor)).lower(),
            }
            products.append(product)
            break
        except AttributeError:
            product = hail_mary(soup)
            if not product:
                products.append[product]

    # Secondly Find Products from Forms
    forms = soup.findAll("form")
    for form in forms:
        if form.get("data-product"):
            data = json.loads(form.get("data-product"))
            variants = data['variants']
            for variant in variants:
                product = {
                    "name": variant['name'],
                    "identity": str(variant['id']),
                    "quantity": variant['inventory_quantity'],
                    "vendor": data['vendor'],
                }
                products.append(product)

    # Thirdly Find Products from Divs
    divs = soup.findAll("div", {"class": "product-json"})
    for div in divs:
        data = json.loads(div.text)
        variants = data['variants']
        for variant in variants:
            product = {
                "name": variant['name'],
                "identity": str(variant['id']),
                "quantity": variant['inventory_quantity'],
                "vendor": data['vendor'],
            }
            products.append(product)

    # Forthly Find Products from Spans
    spans = soup.findAll("span", {"class": "product-json"})
    for span in spans:
        data = json.loads(span.text)
        variants = data['variants']
        for variant in variants:
            product = {
                "name": variant['name'],
                "identity": str(variant['id']),
                "quantity": variant['inventory_quantity'],
                "vendor": data['vendor'],
            }
            products.append(product)
    return products
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re
import json

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


def depth(starts, finishes):
    depth = 1
    startind = 0
    finind = 0
    tups = []
    finishes = [x for x in finishes if x > starts[0]]
    curstart = starts[startind]
    while True:
        if startind == (len(starts) - 1): 
            tups.append((starts[0], finishes[0]))
            break
        if starts[startind + 1] < finishes[finind]: 
            depth += 1
            startind += 1
        else: 
            depth -= 1
            finind += 1
            if depth == 0:
                tups.append((curstart, finishes[finind - 1]))
                starts = starts[startind + 1:]
                finishes = finishes[finind:]
                startind = 0
                finind = 0
                depth = 1
                curstart = starts[startind]
    return tups


def get_variants(link):
    body = requests.get(link).text
    s = [x.start() for x in re.finditer('{', body)]
    f = [x.start() for x in re.finditer('}', body)]
    pairs = depth(s,f)
    idquants = []
    for x, y in pairs:
        try:
            if x+1 == y:
                continue
            bodysec = body[x:y+1]
            if "inventory_quantity" not in bodysec:
                continue
            testjson = json.loads(bodysec)
            if 'variants' in testjson.keys():
                for variant in testjson['variants']:
                    idquants.append(variant)
            elif 'inventory_quantity' in testjson.keys():
                idquants.append(testjson)
            elif 'product' in testjson.keys():
                product = testjson['product']
                if 'inventory_quantity' in product.keys():
                    idquants.append(product)
                if 'variants' in product.keys():
                    for variant in product['variants']:
                        if 'inventory_quantity' in variant.keys():
                            idquants.append(variant)
            else:
                print(testjson.keys())
                print()
        except:
            return idquants
    return idquants


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

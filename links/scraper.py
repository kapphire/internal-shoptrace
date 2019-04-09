import re
import json
import requests

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

# link = "https://www.vivehealth.com/products/memory-foam-mattress-topper"
link = "https://hotsaletools.com/products/tool-33"

result = get_variants(link)
print(result)
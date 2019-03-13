import re
import json
import requests

body = requests.get('https://www.weekliss.com/products/dust-filter-mask').text

teststart = [x.start() for x in re.finditer('{', body)]
testclose = [x.start() for x in re.finditer('}', body)]

def depth(starts, finishes):
    depth = 1
    startind = 0
    finind = 0
    tups = []
    curstart = starts[startind]
    while True:
        if startind == (len(starts) - 1):
            tups.append((starts[0], finishes[-1]))
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

pairs = depth(teststart, testclose)

for x, y in pairs:
    try: 
        testjson = json.loads(body[x:y+1])
    except Exception as e:
        continue
    if 'inventory_quantity' in testjson.keys():
        print('id: ', testjson['id'], '\ntitle: ', testjson['title'], '\nquantity: ', testjson['inventory_quantity'])
        print()

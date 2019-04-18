# import psycopg2
import operator
from functools import reduce
import pandas as pd
import numpy as np
from django.db.models import Count, Q
from links.models import Product, Inventory

# db_url = 'postgres://mmxccvygngqncs:c576723b7f4ce7ac03f4c9dfb9450e87459bd0a14a12768bf46a880a2aceea19@ec2-54-197-232-203.compute-1.amazonaws.com:5432/d2flo5485f32gb'

# conn = psycopg2.connect(db_url)
# cur = conn.cursor()

# tables = pd.read_sql('SELECT table_schema,table_name FROM information_schema.tables ORDER BY table_schema,table_name;', conn)
# links = pd.read_sql('SELECT * FROM links_link', conn)
# inventory = pd.read_sql('SELECT * FROM links_inventory', conn)

# conn.close()
# links.head()

def getchange(col):
    toret = []
    for past, present in zip(col.index[:-1], col.index[1:]):
        change = col[present] - col[past]
        if change > 0:
            change = 0
        toret.append(change)
    return pd.Series(toret, index = col.index[1:])


def relchange(col):
    sensitivity = 0
    toret = [min(0, col.values[0] + col.values[1])]
    for ts in col.index[1:]:
        toret.append(min(0, toret[-1] + col[ts] - sensitivity))
    return pd.Series(toret, index = col.index)


def cusum(df):
    changes = df.apply(getchange)
    
    meanchange = changes.replace(0, np.nan).mean(axis = 1, skipna = True).fillna(0)
    stdchange = changes.replace(0, np.nan).std(axis = 1, skipna = True).replace(0, np.nan).fillna(1)
    
    normed_change = changes.apply(lambda x:(x - meanchange[x.name])/stdchange[x.name], axis = 1)
    # print("NORMED:")
    # print(normed_change[changed])
    # print()
    
    normed_change = normed_change * (normed_change < 0)
    # print("NORMED CLIPPED:")
    # print(normed_change[changed])
    retdf = normed_change.apply(relchange)
    
    retseries = pd.Series(retdf.iloc[-1, :])
    # print(retdf.loc[:, changed])
    # print('============================ CuSum Script')
    # print(retseries)
    
    return retseries

def get_kieran_result():
    products = Product.objects.filter(link__deprecated=False).annotate(c=Count('inventory')).filter(c__gt=2)
    condition = reduce(operator.or_, [Q(product=s) for s in products])
    inventory = pd.DataFrame(Inventory.objects.filter(condition).values())
    inventory['created'] = inventory['created'].apply(pd.to_datetime).dt.round('120min')
    pivoted = pd.pivot_table(inventory, values = 'qty', index = 'created', columns = 'product_id').sort_index()
    changed = pivoted.describe().transpose().query('std != 0').index
    return cusum(pivoted[changed]).sort_values()

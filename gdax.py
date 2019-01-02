import sys
import time
import urllib2
import json

input = {
    "BTC-USD": {"ask": 1000, "bid": 990},
    "BTC-EUR": {"ask": 1200, "bid": 1150},
    "ETH-USD": {"ask": 200, "bid": 180},
    "ETH-EUR": {"ask": 220, "bid": 210},
    "BTC-ETH": {"ask": 5, "bid": 4.5}}




def build_graph(input_map):
    incre_id = 0
    key_to_id = {}
    for k in input_map:
        left, right = k.split('-')
        if left not in key_to_id:
            key_to_id[left] = incre_id
            incre_id += 1
        if right not in key_to_id:
            key_to_id[right] = incre_id
            incre_id += 1
    graph = [[0 for _ in xrange(incre_id)] for _ in xrange(incre_id)]
    for k, v in input_map.iteritems():
        left, right = k.split('-')
        ask = v['ask']
        bid = v['bid']
        left_i = key_to_id[left]
        right_i = key_to_id[right]
        # put into graph
        graph[right_i][left_i] = 1.0 / ask
        graph[left_i][right_i] = bid

    print key_to_id
    for l in graph:
        print l
    return graph, key_to_id


res = (0, 0, [])  # ratio, hops_count


def traverse(graph, current_index, target_index, ratio, hops_cnt, path):
    global res
    if current_index == target_index:
        if res[0] < ratio:
            res = (ratio, hops_cnt, path[:])
        elif res[0] == ratio and res[1] > hops_cnt:
            res = (ratio, hops_cnt, path[:])
        return
    for i in xrange(len(graph)):
        # i is the col
        if current_index == i:
            continue
        if i in path:
            continue
        path.append(i)
        traverse(graph, i, target_index, ratio * graph[current_index][i], hops_cnt+1, path)
        path.pop()

#@req = urllib2.Request("https://api.gdax.com/products", {}, {'Content-Type': 'application/json'})
req = urllib2.Request("https://api.gdax.com/products")
f = urllib2.urlopen(req)
r_json = None
for x in f:
    r_json = json.loads(x)
    break
products = []
for item in r_json:
    products.append(item['id'])
print len(products)

time.sleep(1)
input = {}
for product in products:
    time.sleep(1)
    url = "https://api.gdax.com/products/%s/ticker"
    req = urllib2.Request(url % product)
    f = urllib2.urlopen(req)
    r_json = None
    for x in f:
        r_json = json.loads(x)
        break
    input[product] = {'ask': float(str(r_json["ask"])), 'bid': float(str(r_json['bid']))}

start_name, end_name = "USD", "EUR"
graph, key_to_id = build_graph(input)
traverse(graph, key_to_id[start_name], key_to_id[end_name], 1, 0, [key_to_id[start_name]])
res = float("{0:.5f}".format(res[0])), res[1], res[2]
print res

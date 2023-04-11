import json

data = ''
with open('PVLapLink copy.json') as f:
    data = json.load(f)
    
for item in data:
    item['ProductLink'] = 'https://phongvu.vn/' + item['ProductLink'].split('/')[1]

tmp = json.dumps(data)
with open('Final.json',"w") as f:
    f.write(tmp)
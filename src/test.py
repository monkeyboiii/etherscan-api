import json

file = 'D:\\SUSTech\\3-1\\blockchain\\out\\test.json'

data = {
    'nostril': 'huge',
    'facepalm': 'small'
}

with open(file, 'w') as f:
    json.dump(data, f)
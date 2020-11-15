import csv

file = 'D:\\SUSTech\\3-1\\blockchain\\data\\etherscan\\export-verified-contractaddress-opensource-license.csv'
line = 40

with open(file, 'r') as f:
    cr = csv.reader(f)
    for row in cr:
        print(row)
        line = line - 1
        if line == 0:
            break

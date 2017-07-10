# coding: utf-8
import json
import csv
import ast

def print_tree(datalist):
    try:
        temp_list = datalist[:]
        for s in temp_list[0]:
            if not s:
                datalist[0].remove(s)

        empty = 0
        for lista in datalist[0]:
            if lista:
                empty += 1
        if empty == 0:
            return

        result = {}
        firsts = []
        for m in datalist:
            for n in m:
                firsts.append(n[0])
        firsts = list(set(firsts))
        for i in firsts:
            temp = []
            for j in datalist:
                for l in j:
                    #print
                    #print i, j[0]
                    if i == l[0]:
                        s = l[:]
                        s.pop(0)
                        temp.append(s)
                result[i] = print_tree([temp])
        return result
    except Exception as e:
        print e, datalist

print('Loading data from labels.csv...')
theList = []
with open('labels.csv', mode='r') as infile:
    csvreader = csv.reader(infile)
    next(csvreader)
    for rows in csvreader:
        cat = ast.literal_eval(rows[1])
       
        if cat not in theList:
            theList.append(cat)

# Uncomment the following code block if you want included the ASINs. Use theListASIN list.
#
#print('Loading data from labels.csv...')
#theListASIN = []
#with open('labels.csv', mode='r') as infile:
#    csvreader = csv.reader(infile)
#    next(csvreader)
#    for rows in csvreader:
#        cat = ast.literal_eval(rows[1])
#
#        cat.append(rows[0])
#        theListASIN.append(cat)
print('Data have been loaded successfully!\nExporting data to JSON file...')

with open('export_labels_tree.json', 'w') as outfile:
    json.dump({'root':print_tree([theList])}, outfile, sort_keys=True, indent=4)

# Uncomment the following two lines if you want included the catogories but also the ASINs
# If that is your choice, keep in ming that it will take some time to export a tree with ~253k paths  
#with open('export_labels_ASINs_tree.json', 'w') as outfile:
#    json.dump({'root':print_tree([theListASIN])}, outfile, sort_keys=True, indent=4)
print('JSON file is ready!')

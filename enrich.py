import gzip
import csv
import ast

labels_dictionary = {}
with open('labels.csv', mode='r') as infile:
    csvreader = csv.reader(infile)
    next(csvreader)
    for rows in csvreader:
        labels_dictionary[rows[0]] = ast.literal_eval(rows[1])

def parse(filename):
    f = gzip.open(filename, 'r')
    entry = {}
    for l in f:
        l = l.strip()
        colonPos = l.find(':')
        if colonPos == -1:
            yield entry
            entry = {}
            continue
        eName = l[:colonPos]
        rest = l[colonPos+2:]
        entry[eName] = rest
        if eName == 'product/productId':
            entry['product/categories'] = labels_dictionary[rest]    
    yield entry

if __name__ == "__main__":
    try:
        print ("Parsing data...\nPlease be patient, this will take a while...")
        with gzip.open('output.txt.gz', 'wb') as fo:
            for e in parse("movies.txt.gz"):
                for i in e:
                    fo.write('%s: %s\n' % (i, e[i]))
                fo.write("\n")
        print ("New enriched dataset has been exported successfully!")
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst

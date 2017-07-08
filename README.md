# Addition of ground truth labels on Amazon movie reviews dataset

<img src="http://i.imgur.com/W5KG8qQ.png" alt="labels cloud" style="width: 100px;"/>

## What is it?

This is a side project for my thesis "Classification/Clustering Techniques for Large Web Data Collections".

My main goal was to provide a new, enriched, ground truth labeled dataset to the Machine Learning community. 
All labels have been collected by crawling/scraping Amazon.com for a period of some months. 
By labels I mean the categories in which the products are classified (look the green underlined labels on the screenshot below).

![Image](http://i.imgur.com/mAiuoO6.png)

Please, feel free to make any contributions you feel will make it better.

## The original dataset

All the collected data (for every ASIN of the SNAP Dataset, ~253k products for ~8m reviews) are stored in a csv file ```labels.csv``` in the following format:

- ASIN: unique identifier for the product
- Categories: [label<sub>0</sub>, label<sub>1</sub>, label<sub>2</sub>,..., label<sub>n</sub>]

The [Amazon Movies Reviews dataset](https://snap.stanford.edu/data/web-Movies.html) consists of 7,911,684 reviews Amazon users left between Aug 1997 - Oct 2012.

Data format:

product/productId: _B00006HAXW_

review/userId: _A1RSDE90N6RSZF_

review/profileName: _Joseph M. Kotow_

review/helpfulness: _9/9_

review/score: _5.0_

review/time: _1042502400_

review/summary: _Pittsburgh - Home of the OLDIES_

review/text: _I have all of the doo wop DVD's and this one is as good or better than the 1st ones. Remember once these performers are gone, we'll never get to see them again. Rhino did an excellent job and if you like or love doo wop and Rock n Roll you'll LOVE this DVD!!_

where:
- product/productId: asin, e.g. [amazon.com/dp/B00006HAXW](http://www.amazon.com/dp/B00006HAXW)
- review/userId: id of the user, e.g. [A1RSDE90N6RSZF](http://www.amazon.com/gp/cdp/member-reviews/A1RSDE90N6RSZF)
- review/profileName: name of the user
- review/helpfulness: fraction of users who found the review helpful
- review/score: rating of the product
- review/time: time of the review (unix time)
- review/summary: review summary
- review/text: text of the review

## Instructions 

You can follow the steps mentioned below on how to get the enriched dataset: 
1. Download the original dataset from the [SNAP website](https://snap.stanford.edu/data/web-Movies.html) (~ 3.3 GB compressed) and put it in the root folder of the repository (where you can find also the  ```labels.csv``` file).
2. Execute the python file ```enrich.py```, so the new enriched multi-labeled dataset be exported. The name of the new file should be ```output.txt.gz```.
_Notice: Please be patient s the python script take a while to parse all these reviews._

The python script generates a new compressed file that is actually same with the original one, but with an extra feature (product/categories).

In fact,(the python script) applies a mapping between ASIN values in both files and adds the labels data of the product in every review instance of that, as an extra column.

Here is the code:
```markdown
import gzip
import csv
import ast

def look_up(asin, diction):
    try:
        return diction[asin]
    except KeyError:
        print asin
        return []

def load_labels():
    labels_dictionary = {}
    with open('labels.csv', mode='r') as infile:
        csvreader = csv.reader(infile)
        next(csvreader)
        for rows in csvreader:
            labels_dictionary[rows[0]] = ast.literal_eval(rows[1])
    return labels_dictionary

def parse(filename):
    labels_dict = load_labels()
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
            entry['product/categories'] = look_up(rest, labels_dict)   
    yield entry

if __name__ == "__main__":
    try:
        print ("Parsing dataset...\nPlease be patient, this will take a while...")
        with gzip.open('output.txt.gz', 'wb') as fo:
            for e in parse("movies.txt.gz"):
                for i in e:
                    fo.write('%s: %s\n' % (i, e[i]))
                fo.write("\n")
        print ("New enriched dataset has been exported successfully!\nFile name: output.txt.gz")
    except Exception as inst:
        print type(inst)
        print inst.args
        print inst
```

## The new labeled dataset

The new data format will be:

product/productId: _B00006HAXW_

review/userId: _A1RSDE90N6RSZF_

review/profileName: _Joseph M. Kotow_

review/helpfulness: _9/9_

review/score: _5.0_

review/time: _1042502400_

review/summary: _Pittsburgh - Home of the OLDIES_

review/text: _I have all of the doo wop DVD's and this one is as good or better than the 1st ones. Remember once these performers are gone, we'll never get to see them again. Rhino did an excellent job and if you like or love doo wop and Rock n Roll you'll LOVE this DVD!!_

**product/categories: _['CDs & Vinyl', 'Pop', 'Oldies', 'Doo Wop']_**

## Credits:

If you publish articles based on this dataset, please cite the following paper:

- J. McAuley and J. Leskovec. [From amateurs to connoisseurs: modeling the evolution of user expertise through online reviews](http://i.stanford.edu/~julian/pdfs/www13.pdf). WWW, 2013.

Bibtex is also available:

```
@inproceedings{McAuley:2013:ACM:2488388.2488466,
 author = {McAuley, Julian John and Leskovec, Jure},
 title = {From Amateurs to Connoisseurs: Modeling the Evolution of User Expertise Through Online Reviews},
 booktitle = {Proceedings of the 22Nd International Conference on World Wide Web},
 series = {WWW '13},
 year = {2013},
 isbn = {978-1-4503-2035-1},
 location = {Rio de Janeiro, Brazil},
 pages = {897--908},
 numpages = {12},
 url = {http://doi.acm.org/10.1145/2488388.2488466},
 doi = {10.1145/2488388.2488466},
 acmid = {2488466},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {expertise, recommender systems, user modeling},
} 
```
[//]: # "For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/)."

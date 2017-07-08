## Welcome to GitHub Pages

*This data was originally published on [SNAP](https://snap.stanford.edu/data/web-Movies.html).*

You can use the [editor on GitHub](https://github.com/bazakoskon/labels-on-Amazon-movie-reviews-dataset/edit/master/README.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
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
```
# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/bazakoskon/labels-on-Amazon-movie-reviews-dataset/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.

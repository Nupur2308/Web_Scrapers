import urllib
from BeautifulSoup import *

fhand = open("walmart_links.txt")
urls = []
for line in fhand:
    urls.append(line.rstrip('\n'))
fhand.close()
i = 0

#print urls
reviews = []
for url in urls:
    lis = []
    text = []
    if i == 100: break
    print urls[i]
    html = urllib.urlopen(urls[i]).read()
    soup = BeautifulSoup(html)
    for item in soup.findAll('div','stars customer-stars'):
        for post in item.findAll('span','customer-review-date hide-content-m'):
            lis.append(str(post.contents[0]))
    for item in soup.findAll('p','js-customer-review-text'):
        text.append(str(item.contents[0]))
    for j in range(len(lis)):
        pair = []
        pair.append(lis[j])
        pair.append(text[j])
        reviews.append(pair)
    i += 1

fh = open("rawtext.txt","w")
for r in reviews:
    fh.write(r[0]+'@'+r[1]+'\n')

fh.close()

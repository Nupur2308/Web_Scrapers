import urllib
from bs4 import BeautifulSoup
import urllib2
import pandas as pd
import re
import sys
reload(sys)
sys.setdefaultencoding('UTF8')

fhand = open("amazon_links.txt")
urls = []
for line in fhand:
    urls.append(line.rstrip('\n'))
fhand.close()

i = 0
text = []
name = []
rating = []
date = []

for url in urls:
    # Change the below condition based on which page you want to end the scrape
    if i ==150: break
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    try:
        response = opener.open(urls[i])
    except:
        i += 1
        continue
    html = response.read()
    soup = BeautifulSoup(html,'lxml')
    #review text
    for r in soup.findAll('span',attrs="a-size-base review-text"):
        try:
            edited_text = (re.search('xa0(.+)',str(r.contents)).group(1))
        except:
            edited_text = str(r.contents)
        #cleaning up review text below
        edited_text = edited_text.replace("""u'""","")
        edited_text = edited_text.replace('''u"''',"")
        edited_text = edited_text.replace("""',""","")
        edited_text = edited_text.replace('''",''',"")
        edited_text = edited_text.replace("""']""","")
        edited_text = edited_text.replace('''"]''',"")
        edited_text = edited_text.replace("[","")
        edited_text = edited_text.replace('<br/>,',"")
        edited_text = edited_text.encode().decode('unicode_escape')
        edited_text = edited_text.encode('utf-8')
        text.append(edited_text)

    #author
    for a in soup.findAll('span',attrs="a-size-base a-color-secondary review-byline"):
        if a.find(class_="a-size-base a-link-normal author"):
            edited_author = (re.search('">(.+?)</a>',str(a.contents[2])).group(1)).encode('utf-8')
            name.append(edited_author)

    #rating
    for ra in soup.findAll('i',attrs={'data-hook':"review-star-rating"}):
        rating.append(float(re.search('>(.+?)out',str(ra.contents)).group(1)))

    #date
    for ra in soup.findAll('span',attrs={'data-hook':"review-date"}):
        edited_date = str(ra.contents)
        date.append(edited_date[6:-2])

    print ("Page",i+1)
    i += 1

df = pd.DataFrame({'Author':name,
                    'Rating':rating,
                    'Review text':text,
                    'Review date':date})

writer = pd.ExcelWriter('Amazon_reviews_output.xlsx',engine='xlsxwriter') #putting reviews in one file
df.to_excel(writer,sheet_name = 'Sheet1')
writer.save()

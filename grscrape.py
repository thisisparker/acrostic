import json
import requests
import time

from bs4 import BeautifulSoup

gr_url = 'https://www.goodreads.com/quotes?page='

db = []

for page in range(1,100):
    gr = gr_url + str(page)
    res = requests.get(gr)
    soup = BeautifulSoup(res.text, 'lxml')

    quotes = soup.findAll("div", {"class":"quoteText"})

    print('fetching page {page}'.format(**locals()))

    for q in quotes:
        text = q.get_text(' ', strip=True).split('―')[0].strip().strip('“”')

        try:
            author = q.find('span', {'class':'authorOrTitle'}).get_text().strip().rstrip(',')
            work = q.find('a', {'class':'authorOrTitle'}).get_text().strip()

        except:
            continue

        quote = {'quote':text,'author':author,'work':work}

        #print(quote['quote'], '—', f'{author}, {work}', end='\n\n')

        db.append(quote)

    time.sleep(1.5)

with open('quotes.json', 'a') as f:
    json.dump(db, f, indent=4)

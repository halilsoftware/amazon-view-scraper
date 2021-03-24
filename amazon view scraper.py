import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook

#url = 'https://www.amazon.com/Sennheiser-Momentum-Cancelling-Headphones-Functionality/product-reviews/B07VW98ZKG/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1'
reviewlist = []
def get_soup(url):
    r = requests.get('http://localhost:8050/render.html',params={'url': url,'wait':2})
    soup = BeautifulSoup(r.text,'html.parser')
    return soup
def get_reviews(soup):
    reviwes = soup.find_all('div',{'data-hook':'review'})
    try:
        for item in reviwes:
            reviwe = {
            'product':soup.title.text.replace('Amazon.co.uk:Customer reviews:',''),
            'title' :item.find('a',{'data-hook':'review-title'}).text.strip(),
            'rating' : float(item.find('i',{'data-hook':'review-star-rating'}).text.replace('out of 5 stars','').strip()),
            'body' : item.find('span',{'data-hook':'review-body'}).text.strip()
            }
            reviewlist.append(reviwe)
    except:
        pass
for x in range (1,999):
    soup = get_soup(f'https://www.amazon.com/One-Bag-Plastic-Poker-Chips/product-reviews/B00362L0H6/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    print(f'Getting paga:{x}')
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find('li',{'class':'a-disabled a-last'}):
        pass
    else:
        break
df = pd.DataFrame(reviewlist)
df.to_excel('a6400-reviews.xlsx',index=False)
print('Fin.')
#!/usr/bin/env python
# coding: utf-8

# In[7]:


import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    r = requests.get(url)
    return r.text

def get_pages_num(html):
    soup = BeautifulSoup(html, 'lxml')
    pages_num = soup.find('li', class_='current').text.split('of')[1]
    return int(pages_num)

def write_csv(data):
    with open('parser.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        writer.writerow((data['title'],
                         data['url'],
                         data['price'],
                         data['availability']))
    

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    books = soup.find('ol', class_='row').find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    for book in books:
        title = book.find('h3').find('a').get('title')
        url = 'http://books.toscrape.com/catalogue/' + book.find('h3').find('a').get('href')
        price = book.find('div', class_='product_price').find('p', class_='price_color').text
        availability = book.find('div', class_='product_price').find('p', class_='instock availability').text.strip()
        
    data = {'title' : title,
            'url' : url,
            'price' : price,
            'availability' : availability}
        
    write_csv(data)

def main():
    url = 'http://books.toscrape.com/catalogue/page-1.html'
    base_url = 'http://books.toscrape.com/catalogue/page-'   
    pages_num = get_pages_num(get_html(url))
    for i in range(1,pages_num+1):
        url_gen = base_url + str(i) + '.html' 
        html = get_html(url_gen)
        get_page_data(html)
        
if __name__ == '__main__':
    main()


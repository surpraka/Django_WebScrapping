from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_CRAIGLIST_URL = 'https://delhi.craigslist.org/search/bbb?query= {}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings  = soup.find_all('li', {'class': 'result-row'})
    final_postings = []

    for post in post_listings:
        post_tile = post.find(class_="result-title").text
        post_url =  post.find('a').get('href')
        if(post.find(class_='result-price')):
            post_price = post.find(class_='result-price').text
        else:
            post_price='NA'

        if(post.find(class_='result-image').get('data-ids')):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url= "https://cdn.mos.cms.futurecdn.net/BwL2586BtvBPywasXXtzwA-970-80.jpeg.webp"

        final_postings.append((post_tile,post_url,post_price,post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings':final_postings
    }
    return render(request,'my_app/new_search.html',stuff_for_frontend)

from bs4 import BeautifulSoup
import requests
import httplib2


def get_url_to_img(url):
    getURL = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(getURL.text, 'html.parser')

    # images = soup.findAll('div', class_='sc-e1f8e4dd-5 kUQYWt')
    images = soup.findAll('div', class_='sc-e1f8e4dd-5 kUQYWt')

    for i in str(images).split():
        if 'src=' in i:
            image_url = 'https://ozerki.ru'+i[5:len(i) - 1]
            print(image_url.replace('amp;', '').replace('amp;', ''))
            h = httplib2.Http('.cache')
            response, content = h.request(image_url.replace('amp;', '').replace('amp;', ''))
            out = open('images\img.jpg', 'wb')
            out.write(content)
            out.close()


url = 'https://ozerki.ru/sankt-peterburg/catalog/product/faykompa-tab-p-p-o-6mg-28/'
get_url_to_img(url)

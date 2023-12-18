import requests
from bs4 import BeautifulSoup
import httplib2
import src.settings as settings


def find_url(query, city):
    url_query = ('https://www.google.com/search?q=' + query + '+озерки+' + city).replace(' ', '+')
    r = requests.get(url_query)
    soup = BeautifulSoup(r.text, 'html.parser')
    for element in soup.find_all('a'):
        a = element['href']
        if '/url?q=https://ozerki.ru' in a and '/catalog/product/' in a:
            href = a[7:len(a)]
            slash_num = 0
            index = 0
            if city.lower() == 'москва' or 'мск' == city.lower():
                for i in href:
                    if i == '/':
                        slash_num += 1
                    if slash_num == 6:
                        href = href[0:index]
                        return href, 'product'
                    index += 1
            else:
                product_link, citycode = find_url(query, 'мск')
                product_link = str(product_link[34:len(product_link)])
                href = 'https://ozerki.ru/' + settings.CITY_DICTIONARY[city.lower()] + '/catalog/product/' + product_link
                return href, 'product'
        if '/url?q=https://ozerki.ru/' + settings.CITY_DICTIONARY[city.lower()] in a and 'alphabet' in a:
            if city.lower() == 'москва' or 'мск' == city.lower():
                slash_num = 0
                index = 0
                href = a[7:len(a)]
                for i in href:
                    if i == '/':
                        slash_num += 1
                    if slash_num == 6:
                        return href, 'alphabet'
                    index += 1
            else:
                slash_num = 0
                index = 0
                href = a[7:len(a)]
                for i in href:
                    if i == '/':
                        slash_num += 1
                    if slash_num == 7:
                        href = href[0:index]
                        return href, 'alphabet'
                    index += 1


def parce_information_for_bot(url, code):
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if code == 'product':
            all_names = soup.findAll('h1', class_='sc-af7b87e6-1 geivEL')
            all_prices = soup.findAll('div', class_='product-price__base-price')
            all_addresses = soup.findAll('div', class_='sc-605479e2-4 gqLEMG')
            filteredAddresses = []
            for data in all_addresses:
                filteredAddresses.append(data.text)
            addresses_count = len(filteredAddresses)

            filteredNames = []
            filteredPrices = []
            index = 0
            for data in all_names:
                filteredNames.append(data.text)
                filteredPrices.append(all_prices[index].text)
            return f'{filteredNames[0]}:\n {filteredPrices[0]}\n Доступно в {addresses_count} аптеках'
        else:
            names = str(soup.findAll('a', class_='sc-4a528871-0 eypOQs sc-128b053f-1 pvICS product-name'))

            index = 0
            bot_responce = ['Сделайте более подробный запрос лекарства:\n']
            for letter in names:
                if names[index:index + 20] == 'span itemprop="name"':

                    nameindex = 20
                    for i in names[index + 20:len(names)]:
                        if i == '<':
                            bot_responce.append(names[index + 20:index + nameindex] + '\n')
                            break
                        nameindex += 1
                index += 1
            return bot_responce[0:10]
    else:
        return 'Извините, произошла ошибка'


def get_url_to_img(url):
    getURL = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(getURL.text, 'html.parser')
    images = soup.findAll('div', class_=settings.product_div_image_class)

    for i in str(images).split():
        if 'src=' in i:
            image_url = 'https://ozerki.ru' + i[5:len(i) - 1]
            h = httplib2.Http('.cache')
            response, content = h.request(image_url.replace('amp;', '').replace('amp;', ''))
            out = open('images\img.jpg', 'wb')
            out.write(content)
            out.close()

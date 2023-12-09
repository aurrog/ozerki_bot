import requests
from bs4 import BeautifulSoup
import datetime
import httplib2


def load_logs(message):
    file = open('user_data.txt', 'a', encoding='utf-8')
    data = f'{str(message.from_user.id)}, {str(message.from_user.username)}, {message.from_user.first_name}, {message.from_user.last_name}:   {message.text}      {datetime.datetime.today()}\n'
    file.write(data)

    file.close()


def find_url(query):
    try:
        r = requests.get('https://www.google.com/search?q=' + query + '+озерки+спб')
        soup = BeautifulSoup(r.text, 'html.parser')
        for element in soup.find_all('a'):
            a = element['href']
            if '/url?q=https://ozerki.ru/sankt-peterburg/catalog/product/' in a:
                href = a[7:len(a)]
                slash_num = 0
                index = 0
                for i in href:
                    if i == '/':
                        slash_num += 1
                    if slash_num == 7:
                       href = href[0:index]
                       break
                    index += 1
                return href
    except:
        return 'error'


def parce_information_for_bot(url):
    if url != 'error':
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            all_names = soup.findAll('h1', class_='sc-461baecd-1 jOLEXy')
            all_prices = soup.findAll('div', class_='product-price__base-price')
            all_addresses = soup.findAll('div', class_='sc-605479e2-4 gqLEMG')
            filteredAddresses = []
            for data in all_addresses:
                filteredAddresses.append(data.text)
            adresses_count = len(filteredAddresses)

            filteredNames = []
            filteredPrices = []
            index = 0
            for data in all_names:
                filteredNames.append(data.text)
                filteredPrices.append(all_prices[index].text)
        except:
            return 'Извините, произошла ошибка'
        else:
            return f'{filteredNames[0]}:\n {filteredPrices[0]}\n Доступно в {adresses_count} аптеках'
    else:
        return 'Извините, произошла ошибка'


def get_url_to_img(url):
    getURL = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(getURL.text, 'html.parser')
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

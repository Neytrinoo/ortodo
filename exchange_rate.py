from urllib import request
from bs4 import BeautifulSoup


def get_html(url):
    try:
        resp = request.urlopen(url)
        return resp.read()
    except Exception as e:
        return False


def parse(html):
    try:
        soup = BeautifulSoup(html, features='xml')
        rubl = soup.findAll('td', class_='weak')
        usd = str(rubl[0]).split('</ins>')[1].split('</td>')[0].replace(',', '.')
        eur = str(rubl[1]).split('</ins>')[1].split('</td>')[0].replace(',', '.')
        return [float(usd), float(eur)]  # Парсинг сайта центробанка и возврат курса доллара и евро
    except Exception as e:
        return False


def main():
    print(parse(get_html('http://cbr.ru')))


if __name__ == '__main__':
    main()

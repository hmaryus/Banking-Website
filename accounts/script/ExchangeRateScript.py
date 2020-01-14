import requests
from bs4 import BeautifulSoup


def get_exchange_rates():
    url = 'https://www.bnr.ro/nbrfxrates.xml'
    source = requests.get(url).text

    soup = BeautifulSoup(source, 'lxml')

    for general_info in soup.find_all('header'):
        g_info = general_info.text.strip().split('\n')
        source, date, *extra = g_info

    result = {"source": source, "date": date, "rates": []}
    for exchange_rates in soup.find_all('rate'):
        infos = exchange_rates.attrs
        rate = exchange_rates.text
        currency = infos[u'currency']
        result["rates"].append({"currency": currency, "rate": rate})
    return result


if __name__ == '__main__':
    print(get_exchange_rates())

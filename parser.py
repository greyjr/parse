import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
	return requests.get(url).text


def write_csv(data):
	with open('olx.csv', 'a', newline="") as f:
		writer = csv.writer(f)
		writer.writerow( (	data['name'],
							data['cost'],
							data['district'],
							data['link']) )


def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')
	ads = soup.find('table', class_='fixed offers breakword redesigned').find_all('tr', class_='wrap')
	

	for ad in ads:
		name = ad.find('strong').text.strip()
		try:
			cost = ad.find('p', class_='price').text.strip()
		except:
			cost = ''
		try:
			district = ad.find('tbody').find('td', class_='bottom-cell').find('span').text.strip()
		except:
			district = ''
		link = ad.find('a', class_='thumb').get('href')

		data = {'name': name, 
				'cost': cost, 
				'district': district, 
				'link': link}
		write_csv(data)


def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	pages = soup.find('div', class_='pager rel clr').find_all('span', class_='item fleft')[-1]
	total_pages = str(pages.find('span')).split('>')[1].split('<')[0]
	return int(total_pages)


def main():
	url = 'https://www.olx.ua/krivoyrog/q-для-новорожденных/?page=1'
	base_url = 'https://www.olx.ua/krivoyrog/q-для-новорожденных/?'
	page_part = 'page='
	total_pages = get_total_pages(get_html(url))
	print(total_pages)
	for i in range(1, 3):
		url_gen = base_url + page_part + str(i)
		html = get_html(url_gen)
		get_page_data(html)

if __name__ == '__main__':
	main()
# -*- coding:utf-8 -*-
from pymongo import MongoClient
import pymongo,datetime

if __name__ == '__main__':
	client = MongoClient('192.168.11.153',27018)
	db = client['RDU_JD']
	col_phone = db['price']
	fin = open('time.txt','r')
	products = fin.read().strip().split('\n\n')
	for product in products:
		url = product.split('\n')[0]
		details = product.split('\n')[1:len(product.split('\n'))+1]
		price_dict = {}
		cnt = 0
		for detail in details:
			time, price = detail.split(' ')
			time = datetime.datetime.strptime(time,'%Y-%m-%d')
			price_dict[str(cnt)] = {'time':time, 'price':price}
			cnt = cnt + 1
		col_phone.insert({'url':url,'prices':price_dict})
	client.close()
	fin.close()
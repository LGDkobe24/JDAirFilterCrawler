# -*- coding:utf-8 -*-
from pymongo import MongoClient
import pymongo
from selenium import webdriver
import selenium
import time
from progressbar import ProgressBar
from datetime import datetime
import random
from selenium.webdriver.common.keys import Keys
import os

def get_tags(driver, url):
	tags = []
	for item in driver.find_element_by_css_selector('.comment-info.J-comment-info').find_element_by_css_selector('.tag-list')\
		.find_elements_by_css_selector('span'):
		tags.append(item.text)
	client = MongoClient('192.168.11.153',27018)
	db = client['RDU_JD']
	col_phone = db['tags']
	col_phone.update({"url":url},{"$set":{"url":url, "tags":tags, "insert2dbtime":datetime.now()}}, upsert=True, Multi=True)
	client.close()
	return tags

def get_comm(driver):
	time.sleep(1)
	comments_dict = []
	for elem in driver.find_elements_by_css_selector(".comment-item"):
		comment_dict = {}
		comment_dict['user-info'] = elem.find_element_by_css_selector('.user-info').text
		comment_dict['user-level'] = elem.find_element_by_css_selector('.user-level').text
		comment_dict['comment-con'] = elem.find_element_by_css_selector('.comment-con').text
		try:
			comment_dict['tag-list'] = elem.find_element_by_css_selector('.tag-list').text
		except:
			pass
		try:
			comment_dict['order-info'] = elem.find_element_by_css_selector('.order-info').text
		except:
			pass
		try:
			elem.find_element_by_css_selector('.comment-star.star5')
			comment_dict['comment_stars'] = 5
		except:
			try:
				elem.find_element_by_css_selector('.comment-star.star4')
				comment_dict['comment_stars'] = 4
			except:
				try:
					elem.find_element_by_css_selector('.comment-star.star3')
					comment_dict['comment_stars'] = 3
				except:
					try:
						elem.find_element_by_css_selector('.comment-star.star2')
						comment_dict['comment_stars'] = 2
					except:
						try:
							elem.find_element_by_css_selector('.comment-star.star1')
							comment_dict['comment_stars'] = 1
						except:
							pass
		if len(comment_dict['comment-con'].strip()) != 0 and len(comment_dict['order-info'].strip()) != 0:
			comments_dict.append(comment_dict)
	#print len(comments_dict)
	return comments_dict

def get_comms(driver, url, i, catg):
	for page in range(27000):
		for j in range(30):
			try:
				driver.find_element_by_css_selector('#comment-'+str(i)+' > div:nth-child(11) > div:nth-child(1) > div:nth-child(1)').find_element_by_link_text('下一页')
				break
			except:
				driver.find_element_by_css_selector('body').send_keys(Keys.DOWN)
		driver.find_element_by_css_selector('body').send_keys(Keys.UP)
		comments_dict = get_comm(driver)
		driver.find_element_by_css_selector('#comment-'+str(i)+' > div:nth-child(11) > div:nth-child(1) > div:nth-child(1)').find_element_by_link_text('下一页').click()
		insert_2_db(url, page, catg, comments_dict)
		os.system('cls')
		print "page:",str(page)
		time.sleep(4)

def insert_2_db(url, page, catg, comments):
	try:
		client = MongoClient('192.168.11.153',27018)
		db = client['RDU_JD']
		col_phone = db['assess']
		col_phone.insert({"url":url, "page":page, "category":catg, "comments":comments, "insert2dbtime":datetime.now()})
		client.close()
	except:
		time.sleep(10)
		client = MongoClient('192.168.11.153',27018)
		db = client['RDU_JD']
		col_phone = db['assess']
		col_phone.insert({"url":url, "page":page, "category":catg, "comments":comments, "insert2dbtime":datetime.now()})
		client.close()

if __name__ == '__main__':
	driver = webdriver.Firefox()
	url = 'https://item.jd.com/1217525.html'
	driver.get(url)
	driver.maximize_window()
	#find assessments
	for i in range(12):
		driver.find_element_by_css_selector('body').send_keys(Keys.DOWN)
	driver.find_element_by_css_selector('#detail > div:nth-child(1) > ul:nth-child(1) > li:nth-child(4)').click()
	#tags
	time.sleep(2)
	get_tags(driver, url)
	#click
	#comments-list > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(3) > a:nth-child(1)
	for catg in [u'中评',u'差评',u'好评']:
		i=1
		while catg not in driver.find_element_by_css_selector('.filter-list > li:nth-child('+str(i)+')').text:
			i = i + 1
		driver.find_element_by_css_selector('.filter-list > li:nth-child('+str(i)+')').click()
		time.sleep(1)
		get_comms(driver, url, i-1, catg)
	#comments
	
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
import selenium.common.exceptions

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
	time.sleep(random.randint(1,30))
	comments_dict = []
	for elem in driver.find_elements_by_css_selector(".comments-item"):
		comment_dict = {}
		comment_dict['comment-con'] = ''
		try:
			comment_dict['user-name'] = elem.find_element_by_css_selector('.user-name').text
		except:
			pass
		try:
			comment_dict['user-level'] = elem.find_element_by_css_selector('.u-vip-level').text
		except:
			pass
		try:
			comment_dict['user-addr'] = elem.find_element_by_css_selector('.u-addr').text
		except:
			pass
		try:
			comment_dict['comment-con'] = elem.find_element_by_css_selector('.p-comment').text
		except:
			pass
		try:
			comment_dict['comment-day'] = elem.find_element_by_css_selector('.comment-day.type-item').text
		except:
			pass
		try:
			comment_dict['comment-time'] = elem.find_element_by_css_selector('.comment-time.type-item').text
		except:
			pass
		try:
			comment_dict['features'] = elem.find_element_by_css_selector('.features.type-item').text
		except:
			pass
		try:
			comment_dict['tags'] = elem.find_element_by_css_selector('.p-tabs').text
		except:
			pass
		try:
			elem.find_element_by_css_selector('.grade-star.g-star5')
			comment_dict['comment_stars'] = 5
		except:
			try:
				elem.find_element_by_css_selector('.grade-star.g-star4')
				comment_dict['comment_stars'] = 4
			except:
				try:
					elem.find_element_by_css_selector('.grade-star.g-star3')
					comment_dict['comment_stars'] = 3
				except:
					try:
						elem.find_element_by_css_selector('.grade-star.g-star2')
						comment_dict['comment_stars'] = 2
					except:
						try:
							elem.find_element_by_css_selector('.grade-star.g-star1')
							comment_dict['comment_stars'] = 1
						except:
							pass
		if len(comment_dict['comment-con'].strip()) != 0:
			comments_dict.append(comment_dict)
	#print len(comments_dict)
	return comments_dict

def get_comms(driver, url, i, catg, page_count):
	print "url: ", url
	pbar = ProgressBar(maxval=page_count).start()
	for j in range(30):
		driver.find_element_by_css_selector('body').send_keys(Keys.DOWN)
	for page in range(page_count):
		#print 'page:', str(page)
		pbar.update(page + 1)
		if (page + 1) % 50 == 0:
			time.sleep(30)
			#try:
				#driver.find_element_by_css_selector('#comment-'+str(i)+' > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)').find_element_by_link_text('下一页')
			#	driver.find_element_by_css_selector('.css3-btn')
			#	print 'hehe'
			#	break
			#except:
			#	driver.find_element_by_css_selector('body').send_keys(Keys.DOWN)
			#	print 'haha'
		for j in range(40):
			driver.find_element_by_css_selector('body').send_keys(Keys.UP)
		comments_dict = get_comm(driver)
		if page == page_count -2 or page_count == 1:
			break
		else:
			try:
				driver.find_element_by_css_selector('#comment-'+str(i)+' > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)').find_element_by_link_text(u'下一页').click()
			except:
				break
		#driver.find_element_by_css_selector('#comment-'+str(i)+' > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)').find_element_by_link_text('下一页').click()
		insert_2_db(url, str(page) + '/' + str(page_count), catg, comments_dict)
		#os.system('cls')
		time.sleep(8)
	pbar.finish()

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

def get_page_count(url):
	client = MongoClient('192.168.11.153',27018)
	db = client['RDU_JD']
	col_phone = db['statics']
	item = col_phone.find_one({"url":url})
	client.close()
	total = item['total']
	good = item['good']
	neutral = item['neutral']
	bad = item['bad']
	pic = item['pic']
	count_dict = {}
	count_dict[u'好评'] = int(good)/10 + 1
	count_dict[u'中评'] = int(neutral)/10 +1
	count_dict[u'差评'] = int(bad)/10 + 1
	return count_dict

if __name__ == '__main__':
	driver = webdriver.Firefox()
	fin = open('target_mem_list.txt','r')
	driver.maximize_window()
	for line in fin:
		url = line.strip()
		count_dict = get_page_count(url)
		driver.get(url)
		#find assessments
		for i in range(12):
			driver.find_element_by_css_selector('body').send_keys(Keys.DOWN)
			
		#driver.find_element_by_css_selector('#detail > div:nth-child(1) > ul:nth-child(1) > li:nth-child(4)').click()
		driver.find_element_by_css_selector('#detail-tab-comm > a:nth-child(1)').click()
		#tags
		time.sleep(2)
		#get_tags(driver, url)
		#click
		for catg in [u'好评', u'中评', u'差评']:
			i=1
			#while catg not in driver.find_element_by_css_selector('.filter-list > li:nth-child('+str(i)+')').text:
			while catg not in driver.find_element_by_css_selector( \
				'#comments-list > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(' + str(i) + ') > a:nth-child(1)').text:
				i = i + 1
			page_count = count_dict[catg]
			driver.find_element_by_css_selector(\
				'#comments-list > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(' + str(i) + ') > a:nth-child(1)').click()
			time.sleep(1)
			get_comms(driver, url, i-1, catg, page_count)
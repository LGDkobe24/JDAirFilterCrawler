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

def abstractCrawl():
	#sub page url
	elem = driver.find_element_by_css_selector("li.normal-list:nth-child(1) > a:nth-child(1)")
	detailPageUrl = elem.get_attribute("href")
	#product info
#prodPromotion > div > div:nth-child(4) > a > span.promotion-item-text.promotion-item-link
def get_basic(driver):
	basic_combo = {}
	basic_combo['title_text'] = driver.find_element_by_css_selector(".title-text").text

	elem = driver.find_element_by_css_selector(".big-price")
	basic_combo['big_price'] = elem.text
	elem = driver.find_element_by_css_selector(".small-price")
	basic_combo['small_price'] = elem.text

	#promotion--click 2 expand
	promo_info = []
	try:
		for i in range(5):
			driver.find_element_by_css_selector('#body').send_keys(Keys.DOWN)
		driver.find_element_by_css_selector('div.promotion-item:nth-child(2) > i:nth-child(1) > span:nth-child(1)').click()
		for elem in driver.find_elements_by_css_selector(".promotion-item-text.promotion-item-link"):
			promo_info.append(elem.text)
	except:
		pass
	basic_combo['promo_info'] = promo_info
	return basic_combo

def get_details(driver):
	driver.find_element_by_css_selector('#detailInfo > p:nth-child(1)').click()
	time.sleep(3)
	driver.find_element_by_css_selector('.tab-lst > li:nth-child(2) > a:nth-child(1)').click()
	detail_info = []
	for elem in driver.find_elements_by_css_selector(".Ptable > tbody:nth-child(1)"):
		detail_info.append(elem.text)
	return detail_info

def get_comm(driver):
	driver.find_element_by_css_selector('#pingjia > p:nth-child(1)').click()
	time.sleep(2)
	#good comm
	driver.find_element_by_css_selector('li.tab-item:nth-child(2) > p:nth-child(1)').click()
	good_count = driver.find_element_by_css_selector('li.tab-item:nth-child(2) > p:nth-child(2)').text
	if good_count > 300:
		flip_count = 1500
	else:
		flip_count = (good_count+10) * 4
	time.sleep(1)
	for i in range(flip_count):
		driver.find_element_by_css_selector('#commentListId').send_keys(Keys.DOWN)
	good_combo = []
	for elem in driver.find_elements_by_css_selector(".assess-flat"):
		assess_dict = {}
		try:
			elem.find_element_by_css_selector('.comment-stars-width5')
			assess_dict['comment_stars'] = 5
		except:
			try:
				elem.find_element_by_css_selector('.comment-stars-width4')
				assess_dict['comment_stars'] = 4
			except:
				try:
					elem.find_element_by_css_selector('.comment-stars-width3')
					assess_dict['comment_stars'] = 3
				except:
					try:
						elem.find_element_by_css_selector('.comment-stars-width2')
						assess_dict['comment_stars'] = 2
					except:
						try:
							elem.find_element_by_css_selector('.comment-stars-width1')
							assess_dict['comment_stars'] = 1
						except:
							pass
		try:
			assess_dict['assess_content'] = elem.find_element_by_css_selector('.assess-content').text
		except:
			assess_dict['assess_content'] = ''
		try:
			assess_dict['pay_date'] = elem.find_element_by_css_selector('.pay-date').text
		except:
			assess_dict['pay_date'] = ''
		try:
			assess_dict['product_type'] = elem.find_element_by_css_selector('.product-type').text
		except:
			assess_dict['product_type'] = ''
		good_combo.append(assess_dict)
	for i in range(2):
		driver.find_element_by_css_selector('#commentListId').send_keys(Keys.UP)
	time.sleep(random.randint(0,5))
	#neutral
	neutral_count = driver.find_element_by_css_selector('li.tab-item:nth-child(3) > p:nth-child(2)').text
	if neutral_count > 300:
		flip_count = 1500
	else:
		flip_count = (neutral_count+10) * 4
	driver.find_element_by_css_selector('li.tab-item:nth-child(2) > p:nth-child(1)').click()
	time.sleep(1)
	for i in range(flip_count):
		driver.find_element_by_css_selector('#commentListId').send_keys(Keys.DOWN)
	neutral_combo = []
	for elem in driver.find_elements_by_css_selector(".assess-flat"):
		assess_dict = {}
		try:
			elem.find_element_by_css_selector('.comment-stars-width5')
			assess_dict['comment_stars'] = 5
		except:
			try:
				elem.find_element_by_css_selector('.comment-stars-width4')
				assess_dict['comment_stars'] = 4
			except:
				try:
					elem.find_element_by_css_selector('.comment-stars-width3')
					assess_dict['comment_stars'] = 3
				except:
					try:
						elem.find_element_by_css_selector('.comment-stars-width2')
						assess_dict['comment_stars'] = 2
					except:
						try:
							elem.find_element_by_css_selector('.comment-stars-width1')
							assess_dict['comment_stars'] = 1
						except:
							pass
		try:
			assess_dict['assess_content'] = elem.find_element_by_css_selector('.assess-content').text
		except:
			assess_dict['assess_content'] = ''
		try:
			assess_dict['pay_date'] = elem.find_element_by_css_selector('.pay-date').text
		except:
			assess_dict['pay_date'] = ''
		try:
			assess_dict['product_type'] = elem.find_element_by_css_selector('.product-type').text
		except:
			assess_dict['product_type'] = ''
		neutral_combo.append(assess_dict)
	for i in range(2):
		driver.find_element_by_css_selector('#commentListId').send_keys(Keys.UP)
	time.sleep(random.randint(0,5))
	#bad
	bad_count = driver.find_element_by_css_selector('li.tab-item:nth-child(4) > p:nth-child(2)').text
	if bad_count > 300:
		flip_count = 1500
	else:
		flip_count = (bad_count+10) * 4
	driver.find_element_by_css_selector('li.tab-item:nth-child(4) > p:nth-child(1)').click()
	for i in range(flip_count):
		driver.find_element_by_css_selector('#commentListId').send_keys(Keys.DOWN)
	bad_combo = []
	for elem in driver.find_elements_by_css_selector(".assess-flat"):
		assess_dict = {}
		try:
			elem.find_element_by_css_selector('.comment-stars-width5')
			assess_dict['comment_stars'] = 5
		except:
			try:
				elem.find_element_by_css_selector('.comment-stars-width4')
				assess_dict['comment_stars'] = 4
			except:
				try:
					elem.find_element_by_css_selector('.comment-stars-width3')
					assess_dict['comment_stars'] = 3
				except:
					try:
						elem.find_element_by_css_selector('.comment-stars-width2')
						assess_dict['comment_stars'] = 2
					except:
						try:
							elem.find_element_by_css_selector('.comment-stars-width1')
							assess_dict['comment_stars'] = 1
						except:
							pass
		try:
			assess_dict['assess_content'] = elem.find_element_by_css_selector('.assess-content').text
		except:
			assess_dict['assess_content'] = ''
		try:
			assess_dict['pay_date'] = elem.find_element_by_css_selector('.pay-date').text
		except:
			assess_dict['pay_date'] = ''
		try:
			assess_dict['product_type'] = elem.find_element_by_css_selector('.product-type').text
		except:
			assess_dict['product_type'] = ''
		bad_combo.append(assess_dict)
	time.sleep(random.randint(0,5))
	assess_combo = {}
	assess_combo['good_combo'] = good_combo
	assess_combo['neutral_combo'] = neutral_combo
	assess_combo['bad_combo'] = bad_combo
	return assess_combo

def insert_2_db(url, basic_combo, detail_info, assess_combo):
	try:
		client = MongoClient('192.168.11.101',27018)
		db = client['JD']
		col_phone = db['air']
		col_phone.insert({"url":url, "basic_combo":basic_combo, "detail_info":detail_info, "assess_combo":assess_combo, "timestamp":datetime.now()})
		client.close()
	except:
		time.sleep(10)
		client = MongoClient('192.168.11.101',27018)
		db = client['JD']
		col_phone = db['air']
		col_phone.insert({"url":url, "basic_combo":basic_combo, "detail_info":detail_info, "assess_combo":assess_combo, "timestamp":datetime.now()})
		client.close()

def check_permute(url):
	client = MongoClient('192.168.11.101', 27018)
	db = client['JD']
	col_phone = db['air']
	if col_phone.find_one({"url":url}) is not None:
		client.close()
		return True
	else:
		client.close()
		return False

if __name__ == '__main__':
	driver = webdriver.Firefox()
	fin = open('JDAir.txt','r')
	for line in fin:
		url = line.strip()
	#url = 'http://item.m.jd.com/product/3311953.html?sid=4f4a9e41bda015097ae6d0f37ac1f21f'
		if check_permute(url):
			continue
		else:
			print url
		driver.get(url)
		driver.maximize_window()
	
		basic_combo = get_basic(driver)
		detail_info = get_details(driver)
		assess_combo = get_comm(driver)
		print "inserting..."
		insert_2_db(url, basic_combo, detail_info, assess_combo)

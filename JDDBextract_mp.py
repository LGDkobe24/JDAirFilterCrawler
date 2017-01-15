# -*- coding:utf-8 -*-
from pymongo import MongoClient
import pymongo
import chardet
import json
from datetime import datetime,date
import sys   #引用sys模块进来，并不是进行sys的第一次加载  


def rem():
	f1 = open('phone.txt','w')
	f2 = open('assess.txt', 'w')
	for item in col_phone.find():
		url = item['url'].strip()
		phone_id = url.split('/')[-1].split('.')[0].strip()
		detail_info = str(item['detail_info']).strip()
		#basic_combo
		basic_combo = item['basic_combo']
		promo_info = str(basic_combo['promo_info']).strip()
		small_price = basic_combo['small_price'].strip()
		big_price = basic_combo['big_price'].strip()
		title = basic_combo['title_text'].strip()
		#write phone info
		f1.write(phone_id + '\t')
		f1.write(title + '\t')
		f1.write(big_price + '\t')
		f1.write(small_price + '\t')
		f1.write(promo_info + '\t')
		f1.write(detail_info + '\t')
		f1.write(url + '\n')
		#assess_combo
		good_combo = item['assess_combo']['good_combo']
		for good in good_combo:
			comment_stars = str(good['comment_stars']).encode('utf-8').strip()
			print chardet.detect(comment_stars)
			product_type = good['product_type'].encode('utf-8').strip()
			print chardet.detect(product_type)
			pay_date = good['pay_date'].encode('utf-8').strip()
			print chardet.detect(pay_date)
			assess_content = good['assess_content'].encode('utf-8').strip()
			print chardet.detect(assess_content)
			f2.write(phone_id + '\t' + assess_content + '\t' + comment_stars + '\t' + product_type + '\t' + pay_date + '\n')
		neutral_combo = item['assess_combo']['neutral_combo']
		for good in neutral_combo:
			comment_stars = str(good['comment_stars']).strip()
			product_type = good['product_type'].strip()
			pay_date = good['pay_date'].strip()
			assess_content = good['assess_content'].strip()
			f2.write(phone_id + '\t' + assess_content + '\t' + comment_stars + '\t' + product_type + '\t' + pay_date + '\n')
		bad_combo = item['assess_combo']['bad_combo']
		for good in bad_combo:
			comment_stars = str(good['comment_stars']).strip()
			product_type = good['product_type'].strip()
			pay_date = good['pay_date'].strip()
			assess_content = good['assess_content'].strip()
			f2.write(phone_id + '\t' + assess_content + '\t' + comment_stars + '\t' + product_type + '\t' + pay_date + '\n')
	f1.close()
	f2.close()
def remrem():
	for item in col_phone.find():
		item.pop('_id')
		url = item['url'].strip()
		phone_id = url.split('/')[-1].split('.')[0].strip()
		f = open(phone_id, 'w')
		f.write(json.dumps(item, cls=CJsonEncoder))
		f.close()

def detail_sort(detail_info):
	if len(detail_info.strip()) == 0:
		return detail_info
	else:
		val = ''
		target = [u'品牌',u'型号',u'双卡机类型',u'机身厚度（mm）',u'机身重量（g）',\
		u'双卡机类型',u'最大支持SIM卡数量',u'4G网络',u'ROM',u'主屏幕尺寸（英寸）',u'前置摄像头',u'后置摄像头',u'指纹识别',u'GPS']
		target_dict = {}
		for item in detail_info.strip().split('\t'):
			item = item + ' '
			name = item.split(' ')[0]
			info = ' '.join(item.split(' ')[1:-1])
			if name.strip() in target:
				if name.strip() not in target_dict:
					target_dict[name.strip()] = info.strip()
				else:
					target_dict[name.strip()] = target_dict[name.strip()] + ' ' + info.strip()
		#for item in target_dict:
			#print item
		#	val = target_dict[item.strip()] + '\t' + val
		for item in target:
			if item in target_dict:
				val = target_dict[item] + '\t' + val
			else:
				val = ' ' + '\t' + val
		return val

class CJsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.strftime('%Y-%m-%d %H:%M:%S')
		elif isinstance(obj, date):
			return obj.strftime('%Y-%m-%d')
		else:
			return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
	reload(sys)  #重新加载sys  
	sys.setdefaultencoding('utf8')  ##调用setdefaultencoding函数
	client = MongoClient('192.168.11.153',27018)
	db = client['JD2']
	col_phone = db['phone']
	f1 = open('phone_mp.txt','w')
	f1.write('phone_id\ttotal\tgood\tneutral\tbad\turl\n')
	for item in col_phone.find():
		url = item['url']
		phone_id = url.split('/')[-1].split('.')[0].strip()
		total = item['total']
		good = item['good']
		neutral = item['neutral']
		bad = item['bad']
		f1.write(phone_id + '\t')
		f1.write(total + '\t')
		f1.write(good + '\t')
		f1.write(neutral + '\t')
		f1.write(bad + '\t')
		f1.write(url + '\n')
	f1.close()
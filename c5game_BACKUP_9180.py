# coding:utf-8
import json
import time
import random
import datetime
import requests
import psycopg2
import pandas as pd
from lxml import etree
import sys
sys.path.insert(0,'../Proxy')
import config as cfg

'''
<<<<<<< HEAD
CREATE TABLE "jiake"."game_igxe_goods" (
  "index" SERIAL PRIMARY KEY,
  "appid" int8,
  "good_name" text COLLATE "default",
  "amount" text COLLATE "default",
=======
CREATE TABLE "jiake"."game_c5game_goods" (
  "index" SERIAL PRIMARY KEY,
  "appid" int8,
  "good_name" text COLLATE "default",
  "amount" float8,
>>>>>>> develop
  "good_status" text COLLATE "default",
  "good_num" int8,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP
  )WITH (OIDS=FALSE);
'''
def get_proxy():
  conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
  cursor = conn.cursor()

  ip_list = []
  try:
      cursor.execute("SELECT content FROM {}.{}".format(cfg.SCHEMA_NAME,cfg.TABLE_NAME))
      result = cursor.fetchall()
      for i in result:
          ip_list.append(i[0])
  except Exception as e:
      print (e)
  finally:
      cursor.close()
      conn.close()
  return ip_list

def get_data(ip_lst):
<<<<<<< HEAD
  circles = [421,25,21,1] # 依次循环次数
  print('current circles \ndota2:sales-{},buying-{}; \nH1Z1:sales-{},buying-{};'.format(*circles))
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
  # dota2
  url = "https://www.igxe.cn/dota2/570"
  for i in range(circles[0]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"is_buying":"0","is_stattrak[]":["0","0"],"price_to":"1","price_to":"1000","sort":"2","ctg_id":"0","type_id":"0","page_no":"{}".format(i+1),
      "page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557025475913"} # 出售
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    save_data2db(r.text)
=======
  circles = [100,100,21,8] # 依次循环次数
  print('current circles \ndota2:sales-{},buying-{}; \nH1Z1:sales-{},buying-{};'.format(*circles))
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
  # dota2
  url = "https://www.c5game.com/dota.html"
  appid = 570
  for i in range(circles[0]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"min":"1","max":"800","k":"","rarity":"","quality":"","hero":"","tag":"","sort":"price.desc",
        "locale":"zh","page":"{}".format(i+1)} # 出售
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    save_data2db(appid,r.text)
>>>>>>> develop
    time.sleep(0.5)

  for i in range(circles[1]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
<<<<<<< HEAD
    querystring = {"is_buying":"1","is_stattrak[]":["0","0"],"price_to":"1","price_to":"1000","sort":"2","ctg_id":"0","type_id":"0","page_no":"{}".format(i+1),
      "page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557026884738"} # 求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    save_data2db(r.text)
    time.sleep(0.5)

  # H1Z1
  url = "https://www.igxe.cn/h1z1/433850"
  for i in range(circles[2]): # 21
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"is_buying":"0","is_stattrak[]":["0","0"],"price_to":"1","price_to":"1000","sort":"2","ctg_id":"0","type_id":"0","page_no":"{}".format(i+1),
      "page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557034298679"} # 出售
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    save_data2db(r.text)
=======
    querystring = {"min":"1","max":"800","only":"on","k":"","rarity":"","quality":"","hero":"","tag":"",
        "sort":"price.desc","page":"{}".format(i+1),"locale":"zh"} # 求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    save_data2db(appid,r.text)
    time.sleep(0.5)

  # H1Z1
  url = "https://www.c5game.com/market.html"
  appid = 433850
  for i in range(circles[2]): # 21
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"min":"1","max":"1000","k":"","rarity":"","quality":"","hero":"","tag":"","sort":"price.desc",
        "appid":"433850","locale":"zh","page":"{}".format(i+1)} # 出售
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    save_data2db(appid,r.text)
>>>>>>> develop
    time.sleep(0.5)

  for i in range(circles[3]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
<<<<<<< HEAD
    querystring = {"is_buying":"1","is_stattrak[]":["0","0"],"price_to":"1","price_to":"1000","sort":"2","ctg_id":"0","type_id":"0","page_no":"{}".format(i+1),
      "page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557026884738"} # 求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    save_data2db(r.text)
    time.sleep(0.5)

def save_data2db(html):
  tree = etree.HTML(html)
  total_pages = tree.xpath('//*[@id="page-content"]/a[3]/@page_no')[0]
  print('current page total {}'.format(total_pages),end='\r')

  goods_names = tree.xpath('//div[@class="dataList"]/a/div[2]/@title')
  amounts = tree.xpath('//div[@class="dataList"]/a/div[3]/div/span/text()')
  amount_subs = tree.xpath('//div[@class="dataList"]/a/div[3]/div/sub/text()')
  good_statuses = tree.xpath('//div[@class="dataList"]/a/div[3]/div[2]/text()')
=======
    querystring = {"min":"1","max":"1000","only":"on","k":"","rarity":"","quality":"","hero":"","tag":"",
         "sort":"price.desc","appid":"433850","locale":"zh","page":"{}".format(i+1)} # 求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    save_data2db(appid,r.text)
    time.sleep(0.5)

def save_data2db(appid,html):
  tree = etree.HTML(html)

  goods_names = tree.xpath('//*[@id="yw0"]/div[1]/ul/li/a/img/@alt')
  good_statuses = tree.xpath('//*[@id="yw0"]/div[1]/ul/li/p[2]/span[1]/text()')
  amounts = tree.xpath('//*[@id="yw0"]/div[1]/ul/li/p[2]/span[1]/span/text()')
  good_nums = tree.xpath('//*[@id="yw0"]/div[1]/ul/li/p[2]/span[2]/text()')
>>>>>>> develop

  lst = []
  for i in range(len(goods_names)):
    goods_name = goods_names[i].replace("'",'')
<<<<<<< HEAD
    good_status = good_statuses[i].split('：')[0]
    good_num = eval(good_statuses[i].split('：')[1])
    lst.append([570,goods_name,amounts[i]+amount_subs[i],good_status,good_num])

  # store valid proxies into db.
  print ("\n>>>>>>>>>>>>>>>>>>>> Insert to database Start  <<<<<<<<<<<<<<<<<<<<<<")
=======
    amount = eval(amounts[i].split(' ')[1])
    good_status = good_statuses[i].split(':')[0].replace("求购价","求购").replace("售价","在售")
    good_num = eval(good_nums[i].split('件')[0])
    lst.append([appid,goods_name,amount,good_status,good_num])

  # store valid proxies into db.
  # print ("\n>>>>>>>>>>>>>>>>>>>> Insert to database Start  <<<<<<<<<<<<<<<<<<<<<<")
>>>>>>> develop
  try:
    conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
    cursor = conn.cursor()
    for i,t in enumerate(lst):
<<<<<<< HEAD
      sql = '''INSERT INTO jiake.game_igxe_goods(appid,good_name,amount,good_status,good_num) VALUES({},'{}','{}','{}',{})'''.format(*t)
=======
      sql = '''INSERT INTO jiake.game_c5game_goods(appid,good_name,amount,good_status,good_num) VALUES({},'{}',{},'{}',{})'''.format(*t)
>>>>>>> develop
      cursor.execute(sql)
      conn.commit()
      # print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"insert successfully."+str(i+1),end='\r')
  except Exception as e:
    raise e
  finally:
    cursor.close()
    conn.close()
<<<<<<< HEAD
  print( ">>>>>>>>>>>>>>>>>>>> Insert to database Ended  <<<<<<<<<<<<<<<<<<<<<<")
=======
  print( ">>>>>>>>>>>>>>>>>>>> Insert to database Ended  <<<<<<<<<<<<<<<<<<<<<<",end='\r')
>>>>>>> develop

if __name__ == '__main__':
  conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
  cursor = conn.cursor()
<<<<<<< HEAD
  sql = "DELETE FROM jiake.game_igxe_goods"
=======
  sql = "DELETE FROM jiake.game_c5game_goods"
>>>>>>> develop
  cursor.execute(sql) # 删除当前数据
  conn.commit()
  cursor.close()
  conn.close()

  ip_list = get_proxy()
  get_data(ip_list)


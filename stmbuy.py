# coding:utf-8
import json
import time
import random
import datetime
import requests
import psycopg2
import pandas as pd
import sys
sys.path.insert(0,'../Proxy')
import config as cfg

'''
CREATE TABLE "jiake"."game_stmbuy_goods" (
  "index" SERIAL PRIMARY KEY,
  "on_seek_price_max" int8,
  "on_seek_price_min" int8,
  "market_name" text COLLATE "default",
  "on_sale_price_max" int8,
  "on_sale_price_min" int8,
  "sale_count" int8,
  "market_price" int8,
  "on_sale_count" int8,
  "on_seek_count" int8,
  "last_price" int8,
  "itime" timestamp(6),
  "utime" timestamp(6),
  "market_hash_name" text COLLATE "default",
  "class_id" text,
  "appid" int8,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP
  )WITH (OIDS=FALSE);

COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."on_seek_price_max" IS '最大求购单价';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."on_seek_price_min" IS '最小求购单价';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."market_name" IS '商品中文名称';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."on_sale_price_max" IS '当前最大售价';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."on_sale_price_min" IS '当前最小售价';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."sale_count" IS '累计出售';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."market_price" IS '市场参考价';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."on_sale_count" IS '当前在售数量';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."on_seek_count" IS '当前求购数量';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."last_price" IS '最近成交价';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."appid" IS '游戏代码';
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
    # crawl website: https://www.stmbuy.com/dota2
    url = "https://api2.stmbuy.com/gameitem/list.json"
    headers = {
      'Origin': "https://www.stmbuy.com",
      'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
      }

    # dota2
    for i in range(35):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"row":"20","page":"{}".format(i+1),"appid":"570","category_id":"","showseek":"1","filter":"{}","sort":"-on_seek_price_max"} # dota2 求购
      r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
      save_data2db(json.loads(r.text))
      time.sleep(0.5)

    time.sleep(5)
    # H1Z1
    for i in range(58):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"row":"20","page":"{}".format(i+1),"appid":"433850","category_id":"","filter":"{}","sort":"-market_price,-on_sale_count"} # H1Z1 出售
      r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
      save_data2db(json.loads(r.text))
      time.sleep(0.5)

    # time.sleep(5)
    # # CS:GO
    # for i in range(100,200):
    #   proxy = {'http': 'http://' + random.choice(ip_lst)}
    #   querystring = {"row":"20","page":"{}".format(i+1),"appid":"730","category_id":"","filter":"{}","sort":"-market_price,-on_sale_count"} # CS:GO 出售
    #   r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    #   save_data2db(json.loads(r.text))
    #   time.sleep(0.5)

def save_data2db(dts):
  count = dts['count']
  page = dts['page']
  print('下一页：{}商品总数：{}'.format(page,count))


  lst = []
  for dt in dts['data']:
    on_seek_price_max = dt.get('on_seek_price_max',0)
    on_seek_price_min = dt.get('on_seek_price_min',0)
    market_name = dt.get('market_name','unknown').replace("'",'')
    on_sale_price_max = dt.get('on_sale_price_max',0)
    on_sale_price_min = dt.get('on_sale_price_min',0)
    sale_count = dt.get('sale_count',0)
    market_price = dt.get('market_price',0)
    on_sale_count = dt.get('on_sale_count',0)
    on_seek_count = dt.get('on_seek_count',0)
    last_price = dt.get('last_price',0)
    itime =  datetime.datetime.fromtimestamp(dt.get('itime',0))
    utime = datetime.datetime.fromtimestamp(dt.get('utime',0))
    market_hash_name = dt.get('market_hash_name','unknown').replace("'",'')
    class_id = dt.get('_id','')
    appid = dt.get('appid',0)

    lst.append([on_seek_price_max,on_seek_price_min,market_name,on_sale_price_max,on_sale_price_min,sale_count,
                market_price,on_sale_count,on_seek_count,last_price,itime,utime,market_hash_name,class_id,appid])
  # new_col = ['on_seek_price_max','on_seek_price_min','market_name','on_sale_price_max','on_sale_price_min',
  #   'sale_count','market_price','on_sale_count','on_seek_count','last_price','itime','utime','market_hash_name']
  # df = pd.DataFrame(lst)
  # df.columns = col_name

  # store valid proxies into db.
  # print ("\n>>>>>>>>>>>>>>>>>>>> Insert to database Start  <<<<<<<<<<<<<<<<<<<<<<")
  try:
    conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
    cursor = conn.cursor()
    for i,t in enumerate(lst):
      sql = '''INSERT INTO jiake.game_stmbuy_goods(on_seek_price_max,on_seek_price_min,market_name,on_sale_price_max,on_sale_price_min,sale_count,
        market_price,on_sale_count,on_seek_count,last_price,itime,utime,market_hash_name,class_id,appid) VALUES({},{}, '{}',{}, {},{}, {},{},
        {}, {},'{}','{}','{}','{}',{})'''.format(*t)
      cursor.execute(sql)
      conn.commit()
      print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"insert successfully."+str(i+1),end='\r')
  except Exception as e:
    raise e
  finally:
    cursor.close()
    conn.close()
  print( ">>>>>>>>>>>>>>>>>>>> Insert to database Ended  <<<<<<<<<<<<<<<<<<<<<<",end='\r')

if __name__ == '__main__':
  conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
  cursor = conn.cursor()
  sql = "DELETE FROM jiake.game_stmbuy_goods"
  cursor.execute(sql) # 删除当前数据
  conn.commit()
  cursor.close()
  conn.close()

  ip_list = get_proxy()
  get_data(ip_list)


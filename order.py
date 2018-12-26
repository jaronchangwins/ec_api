#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by vellhe 2017/7/9
from flask import Flask, request
import os
import datetime
import pymysql
import json

app = Flask(__name__)
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8' 

@app.route("/")
def home():
   return "Jaron"

@app.route('/Buyer/GetList', methods=['POST'])
def BuyerGetList():
  statusId = request.form.get('statusId')
  sql = "SELECT o.order_id as \'OrderId\', o.order_name as \'OrderName\',s.status_name as \'StatusName\' FROM  tb_order o INNER JOIN v_status s ON o.order_status_id = s.status_id where o.order_status_id= \'" + statusId + "\'"
  str_result = getData(sql)
  return str_result

@app.route('/Buyer/GetWaiDeposit', methods=['POST'])
def BuyerGetWaiDeposit():
  orderId = request.form.get('orderId')
  sql="select o.order_id as \'OrderId\' ,o.order_name as \'OrderName\',o.order_desc as \'OrderDesc\',u.user_name as \'Buyer\',o.order_count as \'Count\',p.product_time_name as \'Time\',o.order_total as \'Total\',o.order_deposit as \'Deposit\',o.order_balance as \'Balance\' from tb_order o inner join tb_user u on o.buyer_id = u.user_id  inner join v_product_time p on o.product_time = p.product_time_id where o.order_id= \'" + orderId + "\'"
  str_result = getData(sql)
  return str_result




def EditData(sql):
  conn = pymysql.connect(host = '59.127.224.170', user = 'yali',  passwd = "qazxcdews",  db = 'Purchasing', port = 3307)  
  cur = conn.cursor() 
  cur.execute(sql)
  conn.commit()
  str_result = 'Success'
  return str_result

def getData(sql):
  conn = pymysql.connect(host = '59.127.224.170', user = 'yali',  passwd = "qazxcdews",  db = 'Purchasing', port = 3307) 
 
  cur = conn.cursor() 
  cur.execute(sql)
  num_fields = len(cur.description)
  column_list = [i[0] for i in cur.description]
  str_result = ''
  result = []
  datas = {}
  for row in cur:
    rowdata = {}
    for idx, i in enumerate(column_list, start = 0):
      value = row[idx]
      if type(value) is datetime.datetime:
        rowdata[column_list[idx]] = myconverter(row[idx])
      elif type(value) is int:
        rowdata[column_list[idx]] = str(row[idx]).strip()
      else:
        rowdata[column_list[idx]] = row[idx].strip()
    result.append(rowdata)
  datas['data'] = result
  str_result = json.dumps(datas)
  return str_result


def myconverter(o):
  if isinstance(o, datetime.datetime):
    return o.__str__()


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=1234)

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
   return "台灣獨立"

@app.route('/Admin/GetVendor', methods=['POST'])
def AdminGetVendor():
  typeId = request.form.get('typeId')
  sql = "SELECT v.name as \'VendorName\', v.vid as \'VendorId\' FROM Vendor v INNER JOIN VendorItem vi ON v.vid = vi.vid WHERE vi.item = \'" + typeId + "\'"
  str_result = getData(sql)
  return str_result

@app.route('/Admin/GetVendorPerson', methods=['POST'])
def GetVendorPerson():
  vendorId = request.form.get('vendorId')
  sql = "SELECT vp.name as \'PersonName\', vp.vpid as \'PersonId\', vp.gender as \'PersonGender\', vp.mobile as \'PersonTel\' FROM VendorPersonnel vp INNER JOIN Vendor v ON vp.vid = v.vid WHERE v.vid = \'" + vendorId + "\' AND vp.enable = 1"
  str_result = getData(sql)
  return str_result

@app.route('/Admin/Assign', methods=['POST'])
def AdminAssign():
  pid = request.form.get('pid')
  vpid = request.form.get('vpid')
  sql = "INSERT INTO Assign (pid, vpid) VALUES(\'"+pid+"\',\'"+vpid+"\')" 
  str_result = EditData(sql)
  return str_result

@app.route('/Admin/Projects', methods=['POST'])
def AdminProjects():
  sql = "SELECT p.pid, p.name, mtype.name as \'typeName\', mstatus.name as \'statusName\', p.address, mtimetype.name as \'timetypeName\', p.pdesc, p.amount, p.createTime FROM project p INNER JOIN miscode mtype ON p.type = mtype.miscode AND mtype.misckind = \'project_type\' INNER JOIN miscode mstatus ON p.status = mstatus.miscode AND mstatus.misckind = \'project_status\' INNER JOIN miscode mtimetype on p.time_type = mtimetype.miscode AND mtimetype.misckind= \'time_type\'"
  str_result = getData(sql)
  return str_result

@app.route('/Project/Create', methods=['POST'])
def ProjectCreate():
  name = request.form.get('name')
  ptype = request.form.get('type')
  address = request.form.get('address')
  time_type = request.form.get('time_type')
  m_id = request.form.get('m_id')
  pdesc = request.form.get('pdesc')
  amount = request.form.get('amount')
  ptype = request.form.get('type')
  sql = "INSERT INTO Project (name, type, status, address, time_type, m_id, pdesc, amount, createTime) VALUES(\'"+name+"\',\'"+ptype+"\',\'1000\',\'"+address+"\',\'"+time_type+"\',\'"+m_id+"\',\'"+pdesc+"\', "+amount+", NOW())" 
  str_result = EditData(sql)
  return str_result

@app.route('/Project/MyProjects', methods=['POST'])
def ProjectMyProjects():
  mId = request.form.get('mid')
  sql = "SELECT p.pid, p.name, mtype.name as \'typeName\', mstatus.name as \'statusName\', p.address, mtimetype.name as \'timetypeName\', p.pdesc, p.amount, p.createTime FROM Project p INNER JOIN miscode mtype ON p.type = mtype.miscode AND mtype.misckind = \'project_type\' INNER JOIN miscode mstatus ON p.status = mstatus.miscode AND mstatus.misckind = \'project_status\' INNER JOIN miscode mtimetype on p.time_type = mtimetype.miscode AND mtimetype.misckind= \'time_type\' WHERE mid = "+mId 
  str_result = getData(sql)
  return str_result

@app.route('/Project/Detail', methods=['POST'])
def ProjectDetail():
  pId = request.form.get('pid')
  sql = "SELECT p.pid, p.name, mtype.name as \'typeName\', mstatus.name as \'statusName\', p.address, mtimetype.name as \'timetypeName\', p.pdesc, p.amount, p.createTime FROM Project p INNER JOIN miscode mtype ON p.type = mtype.miscode AND mtype.misckind = \'project_type\' INNER JOIN miscode mstatus ON p.status = mstatus.miscode AND mstatus.misckind = \'project_status\' INNER JOIN miscode mtimetype on p.time_type = mtimetype.miscode AND mtimetype.misckind= \'time_type\' WHERE pid = \'"+pId+"\'" 
  str_result = getData(sql)
  return str_result



def EditData(sql):
  conn = pymysql.connect(host = '127.0.0.1', user = 'root',  passwd = "root",  db = 'master_of_cleaning2') 
  cur = conn.cursor() 
  cur.execute(sql)
  conn.commit()
  str_result = 'Success'
  return str_result

def getData(sql):
  conn = pymysql.connect(host = '127.0.0.1', user = 'root',  passwd = "root",  db = 'master_of_cleaning2') 
 
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
#!/usr/bin/python3
#coding:utf-8
import json
import urllib.request
import sqlite3
import sys
import os

from configparser import ConfigParser

def translate_remote(word):
    """
    YouDao API Key
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path,"translation.ini")
    #: check the existance of the config file
    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
    else:
        print("Config not found!Exiting!")
        sys.exit(1)
    keyfrom = cfg.get("YouDao","keyfrom")
    key = cfg.get("YouDao","key")
    try:
        url = 'http://fanyi.youdao.com/openapi.do?keyfrom='+keyfrom+'&key='+key+'&type=data&doctype=json&version=1.1&q=' + word
        wordinfo = urllib.request.urlopen(url).read().decode('utf-8')
        data = json.loads(wordinfo)
       
        #: if word is exist,the len(data) should be five.
        if len(data) !=5:
            print("Not a word!")
        else:
            translation = ''
            for meaning in data['basic']['explains']:
                print(meaning)
                translation =  translation+meaning+'\n'
            save_word(word,translation)
    finally:
        pass

def save_word(word,translation):
    """
    Save word to database
    """
    conn = sqlite3.connect("python_dict.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE if not exists dict
                      (vocabulary text,translation text)
                   """)
    sql="select * from dict where vocabulary='"+word+"'"
    cursor.execute(sql)
    if cursor.fetchone() == None:
        sql="insert into dict values ('"+word+"','"+translation+"')"
        cursor.execute(sql)
        conn.commit()
        print("save successful!")
    else:
        pass
    cursor.close()
    conn.close()

def translate_local(word):
    """
    search vocabulary from local database
    """
    conn = sqlite3.connect("python_dict.db")
    cursor = conn.cursor()
    sql = "select * from dict where vocabulary='"+word+"'"
    cursor.execute(sql)
    data=cursor.fetchone()
    cursor.close()
    conn.close()
    if data == None:
        print("get translation from YouDao")
        return False
    else:
        print(data[1])
        return True    

def translate_main(word):
    if translate_local(word):
        pass
    else:
       translate_remote(word)
 
if __name__ == "__main__":
    if len(sys.argv)==1:
        print("need a word!")
    else:
        translate_main(sys.argv[1])

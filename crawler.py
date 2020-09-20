#-*- coding: utf-8 -*-

import requests
from datetime import datetime
from ptyz 
import schedule
import time

num = []
parking_place = []
parking_max = []
parking_now = []
now_time = ""

def craw_parking():
    tmp_num = []
    tmp_parking_place = []
    tmp_parking_max = []
    tmp_parking_now = []
    url = "https://www.sisul.or.kr/open_content/parking/guidance/useable.jsp"
    bring = requests.get(url)
    src = bring.text
    start_index = src.find("<tbody>")
    last_index = src.find("</tbody>")
    data_list = src[start_index:last_index]
    data_list = data_list.encode("UTF-8")
    for i in range(31):
        first_data_index = data_list.find("<td>") + 4
        end_data_index = data_list.find(" </td>")
        data_word = data_list[first_data_index:end_data_index]
        tmp_num.append(data_word)
        data_list = data_list[end_data_index+5:]

        first_data_index = data_list.find("<td>") + 4
        end_data_index = data_list.find(" </td>")
        data_word = data_list[first_data_index:end_data_index]
        tmp_parking_place.append(data_word)
        data_list = data_list[end_data_index+5:]

        first_data_index = data_list.find("<td>") + 4
        end_data_index = data_list.find(" </td>")
        data_word = data_list[first_data_index:end_data_index]
        tmp_parking_max.append(data_word)
        data_list = data_list[end_data_index+5:]

        first_data_index = data_list.find("<td>") + 4
        end_data_index = data_list.find(" </td>")
        data_word = data_list[first_data_index:end_data_index]
        tmp_parking_now.append(data_word)
        data_list = data_list[end_data_index+5:]

    current_time = datetime.now(timezone("Asia/Seoul")).strftime("%Y-%m-%d %H")
    return tmp_num, tmp_parking_place, tmp_parking_max, tmp_parking_now, current_time

def craw_weather():
    url = "https://n.weather.naver.com/"
    bring = requests.get(url)
    src = bring.text
    src = src.encode("UTF-8")
    start_index = src.find('<strong class="current"><span class="blind">') + 64
    last_index = src.find('<span class="degree">')
    temperture = src[start_index:last_index]

    return temperture

def save():
    f = open("parking_data.csv", mode="at")
    num, parking_place, parking_max, parking_now, now_time = craw_parking()
    temperture =  craw_weather()
    for i in range(31):
        f.write( "\n" + num[i] + "," + parking_place[i] + "," + parking_max[i] + "," + parking_now[i] + "," + now_time[i] + "," + temperture)
    f.close
    print("[+] save done! " + now_time)
    
    p = open("log.txt", mode="at")
    p.write("save done! " + now_time + "\n")
    p.close()

schedule.every(3600).seconds.do(save)

while True:
    schedule.run_pending()
    time.sleep(1)

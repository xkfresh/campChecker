import os
import shutil
import requests
import json
import datetime
import traceback

from selenium import webdriver
from selenium.webdriver.support.select import Select

SITE_URL = "http://www.muji.net/camp/"
AREA_TEXT = "Cエリア"

LINE_MESSAGE_API = "https://api.line.me/v2/bot/message/push"
LINE_AUTH_TOKEN = "<token>"
LINE_GROUP_ID = "<line group id>"

def handler(event=None, context=None):

    # /tmp/bin 配下に移動
    move_bin("headless-chromium")
    move_bin("chromedriver")

    retStr = "Successed!"

    try:
        options = webdriver.ChromeOptions()
        options.binary_location = '/tmp/bin/headless-chromium'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")

        driver = webdriver.Chrome(executable_path="/tmp/bin/chromedriver",
                                options=options,
                                service_log_path="/tmp/chromedriver.log")
        driver.get(SITE_URL)
        driver.implicitly_wait(1)

        driver.find_element_by_link_text("空き状況を見る").click()
        driver.implicitly_wait(1)
        driver.switch_to.window(driver.window_handles.pop())

        campSite = driver.find_element_by_name("CAMP_JO")
        Select(campSite).select_by_visible_text("無印良品カンパーニャ嬬恋キャンプ場")
        driver.implicitly_wait(1)

        siteYear = driver.find_element_by_name("SITE_YEA")
        siteMonth = driver.find_element_by_name("SITE_MON")
        Select(siteYear).select_by_value('2022')
        Select(siteMonth).select_by_value('8')

        driver.find_element_by_id("SEARCH_SITE_LINK_BTN2").click()
        driver.implicitly_wait(1)
        driver.switch_to.window(driver.window_handles.pop())

        driver.find_element_by_link_text(AREA_TEXT).click()
        driver.implicitly_wait(1)

        seekTRs = driver.find_elements_by_xpath("//*[@id='SiteScroll']/table/tbody/tr")
            
        msg = ""
        for trElement in seekTRs:
            trStrAll = str(trElement.text)
            strList = trStrAll.split("\n")
            noStr = strList[0]
            nameStr = strList[1]
            dateA = "8/12"
            stsStrA = strList[13]
            dateB = "8/13"
            stsStrB = strList[14]
            print("[" + noStr + ", " + dateA + ":" + stsStrA
                        + ", " + dateB + ":" + stsStrB + "]")
            if stsStrA == "●" and stsStrB == "●":
                if msg != "": msg = msg + "\n"
                msg = msg + "[" + noStr + ", " + dateA + ":" + stsStrA + "]"
                msg = msg + "[" + noStr + ", " + dateB + ":" + stsStrB + "]"
            elif stsStrA == "●":
                if msg != "": msg = msg + "\n"
                msg = msg + "[" + noStr + ", " + dateA + ":" + stsStrA + "]"
            elif stsStrB == "●":
                if msg != "": msg = msg + "\n"
                msg = msg + "[" + noStr + ", " + dateB + ":" + stsStrB + "]"

        if  msg != "":
            print(msg)
            sendmsg = "無印良品カンパーニャ嬬恋キャンプ場\n"
            sendmsg = sendmsg + SITE_URL + "\n"
            sendmsg = sendmsg + msg
            # sendMail.sendMails(areaText)
            headers = {'content-type': 'application/json','Authorization': LINE_AUTH_TOKEN}
            requests.post(LINE_MESSAGE_API, headers=headers, data=json.dumps(
                {
                    "to":LINE_GROUP_ID,
                    "messages": [{
                        "type": "text",
                        "text": sendmsg 
                    }]
                }
            ))
        print(datetime.datetime.now())
        driver.quit()
        # driver.implicitly_wait(1)
  
    except Exception:
        retStr = "Failed!"
        t = traceback.format_exc()
        print(t)
    finally:
        # 前回までのコンテキストが再利用されることがあり 'No space left on device' になるのを防ぐ
        remove_unnecessary_file()

    return retStr

def move_bin(fname, src_dir = "/opt", dest_dir = "/tmp/bin"):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    dest_file = os.path.join(dest_dir, fname)
    shutil.copy2(os.path.join(src_dir, fname), dest_file)
    os.chmod(dest_file, 0o775)


def remove_unnecessary_file():
    if os.path.exists('/tmp/bin/'):
        shutil.rmtree('/tmp/bin/')

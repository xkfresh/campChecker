import requests
import json
import datetime
from selenium import webdriver
from selenium.webdriver.support.select import Select

WEB_HOOK_URL = "https://hooks.slack.com/services/xxxxxxxx"

def checkArea(areaText):
    try:
        driver = webdriver.Chrome()
        driver.get("http://www.muji.net/camp/")
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

        driver.find_element_by_link_text(areaText).click()
        driver.implicitly_wait(1)

        seekTRs = driver.find_elements_by_xpath("//*[@id='SiteScroll']/table/tbody/tr")
            
        msg = ""
        for trElement in seekTRs:
            trStrAll = str(trElement.text)
            # print("trStrAll-->>")
            # print(trStrAll)
            # print("trStrAl--<<")
            strList = trStrAll.split('\n')
            # print(strList)
            noStr = strList[0]
            # print("No.")
            print(noStr)
            nameStr = strList[1]
            # print("Name")
            # print(nameStr)
            dateA = "12"
            stsStrA = strList[13] # 2 = 8/1
            print(dateA  + ":" + stsStrA)
            dateB = "13"
            stsStrB = strList[17] # 2 = 8/1
            print(dateB  + ":" + stsStrB)
            if stsStrA == "●":
                msg = msg + "[" + noStr + ":"  + nameStr + "] " + dateA + " "
            if stsStrB == "●":
                msg = msg + "[" + noStr + ":"  + nameStr + "] " + dateB + " "
        if  msg != "":
            print(msg)
            # sendMail.sendMails(areaText)
            requests.post(WEB_HOOK_URL, data=json.dumps(
            {"channel": "#general", "username": "嬬恋キャンプ場", "text": msg,"icon_emoji": ":ghost:"}
            ))
        print(datetime.datetime.now())
        driver.quit()
        driver.implicitly_wait(1)
    except Exception:
        pass

# checkArea("Aエリア")

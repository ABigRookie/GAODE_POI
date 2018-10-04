# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains  # 引入 ActionChains 类
#
# browser = webdriver.Chrome()
# browser.get('https://www.amap.com/place/B000A81K18')
#
# source = driver.find_element_by_id("xx")
#
# # 结束位置：定位到元素要移动到的目标位置
# target = driver.find_element_by_id("xx")
#
# # 执行元素的拖放操作
# ActionChains(driver).drag_and_drop(source,target).perform()

from selenium import webdriver
import requests
browser = webdriver.Chrome()
headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept - Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
            'Connection': 'Keep-Alive',
            'User-Agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36",
        }
browser.get("https://www.amap.com/place/B000A81K18")
cookies = browser.get_cookies()
print(cookies)
s = requests.session()
for cookie in cookies:
    s.cookies.set(cookie['name'],cookie['value'])
r1 = s.get("https://www.amap.com/detail/get/detail?id=B000A83JHK",headers=headers)
print(r1.text)

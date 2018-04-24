from selenium import webdriver
from lxml import etree

driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--load-images=false'])
driver.set_window_size(1280, 2400)
driver.get('http://www.booktxt.net/0_62/')
content = driver.page_source
title = driver.title
print(title)
print(content)
# driver.service.process.send_signal(signal.SIGTERM)
driver.close()
selector = etree.HTML(content)
url = selector.xpath('//*[@id="list"]/dl/dd[9]/following-sibling::dd/a/text()')
print(url)

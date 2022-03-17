import requests
from bs4 import BeautifulSoup

# input: id
# 用硬盘反抗局域网极权
# 「备份豆瓣计划」&「豆瓣跑路计划」& duty machine & Terminus计划
# 长／短评

# movie_url = 'https://push.douban.com:4397/sse?channel=notification:user:153095864&auth=153095864_1646402565:df5e97d91b640a0a06b1f0885900d86d0fa481e0'
url = 'https://www.douban.com/people/153095864/statuses'

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
resp = requests.get(url, headers=headers)
#
bs = BeautifulSoup(resp.text, 'html.parser')
# bs.find_all('div', class_='item')
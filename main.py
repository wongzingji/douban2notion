import requests
from bs4 import BeautifulSoup
from notion import Notion


token = 'secret_M3m1cee3Zcj5nhw6FXd8z1dis4MenvcqTVYcYq3iT5P'
n = Notion(token)

def crawl(url, parent_id):
    headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

    resp = requests.get(url, headers=headers)
    text = resp.text
    bs = BeautifulSoup(text, 'html.parser')

    # title
    title = bs.find('title').text.strip()
    # author
    span = bs.find('span', class_='from')
    author = span.find('a').text
    res = n.create_page(parent_id, title, author)
    page_id = res['id']

    # 正文
    content = bs.find('div', class_='rich-content topic-richtext')
    paragraph = content.find_all('p')

    total_text = ''
    for p in paragraph:
        total_text += p.text + '\n'

    n1 = len(total_text)//1500 + 1
    for i in range(n1):
        chunk = total_text[1500*i:1500*(i+1)]
        n.update_page_content(page_id, chunk)


    # divider
    n.add_block(page_id, 'divider')

    # comment
    comm = bs.find('ul', id='comments')

    usr_lst = []
    h4 = comm.find_all('h4')
    for item in h4:
        usr = item.find('a').text
        usr_lst.append(usr)

    comments = comm.find_all('p', class_='reply-content')

    comm_text = ''
    for i in range(len(comments)):
        comm_text += usr_lst[i]+': '+comments[i].text + '\n'
        comm_text += '------------'+'\n'

    n2 = len(comm_text)//1500 + 1
    for i in range(n2):
        chunk = comm_text[1500*i:1500*(i+1)]
        n.update_page_content(page_id, chunk)


if __name__ == '__main__':
    url = 'https://www.douban.com/group/topic/204745780/'
    db_id = '2c010a7238ff4802a45855c861e84d7d'
    crawl(url, db_id)
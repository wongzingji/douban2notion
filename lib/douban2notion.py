import requests
from bs4 import BeautifulSoup

from .notion import Notion
from .upload import upload_elem, upload_block

class Douban2Notion():
    def __init__(self, token: str):
        self.headers = {
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        } # TODO
        self.n = Notion(token)


    def process_group(self, url: str, parent_id: str):
        resp = requests.get(url, headers=self.headers)
        text = resp.text
        bs = BeautifulSoup(text, 'html.parser')

        # title
        title = bs.find('title').text.strip()
        # author
        span = bs.find('span', class_='from')
        author = span.find('a').text
        res = self.n.create_page(parent_id, title, author, url)
        page_id = res['id']

        resp = requests.get(url, headers=self.headers)
        text = resp.text
        bs = BeautifulSoup(text, 'html.parser')

        # 正文
        content = bs.find('div', class_='rich-content topic-richtext').contents # bs.find('div', {'class': 'rich-content topic-richtext'})
        content = content[1:-1]
        paragraph = ''
        for item in content:
            if item.name in ['p', 'div', 'span', 'ul']:
                paragraph = upload_block(self.n, item, paragraph, page_id)
            else:
                paragraph = upload_elem(self.n, item, paragraph, page_id)

        # append the last text
        if paragraph:
            self.n.add_paragraph(page_id, paragraph)

        # divider
        self.n.add_simple_block(page_id, 'divider')

        # comment
        comments = bs.find('ul', id='comments')
        lis = comments.find_all('li')

        comm_paragraph = ''
        for li in lis:
            user1 = li.find('div', class_='bg-img-green').h4.a.text
            if li.find('div', class_='reply-quote'):
                user2 = li.find('span', class_='pubdate').text
            else:
                user2 = None

            comm = li.find('p', class_='reply-content').text
            if user2:
                comm_paragraph += f'{user1} reply {user2}: {comm}\n'
            else:
                comm_paragraph += f'{user1}: {comm}\n'
            comm_paragraph += '--------------------'+'\n'

        self.n.add_paragraph(page_id, comm_paragraph)
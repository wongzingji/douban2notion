import requests
from bs4 import BeautifulSoup
from notion import Douban2Notion


token = ''
n = Douban2Notion(token)


def process_tag(tag, paragraph, page_id):
    try:
        class_ = tag['class']
    except:
        class_ = None

    try:
        style = tag['style']
    except Exception:
        style = None

    if isinstance(tag, str):
        if paragraph:
            paragraph += '\n' + tag.strip()
        else:
            paragraph += tag.strip()
        return paragraph
    else:
        # 提交text
        if paragraph:
            n.add_paragraph(page_id, paragraph)

        # CASE WHEN
        # heading
        if tag.name != 'hr' and tag.name[0] == 'h':
            type = 'heading_'+'3' if int(tag.name[1:]) > 3 else 'heading_'+tag.name[1:]  # notion只提供3种格式的heading
            n.add_text(page_id, type, tag.text)

        # divider
        elif tag.name == 'hr':
            type = 'divider'
            n.add_simple_block(page_id, type)

        # image
        elif class_ and class_ == 'image-wrapper':
            img_url = tag['src'][:-3] + 'jpg'
            n.add_image(page_id, img_url)

        # image_caption
        elif class_ and class_ == 'image-caption-wrapper':
            type = 'paragraph'
            n.add_text(page_id, type, tag.text)

        # link
        elif tag.name == 'a':
            n.add_link(page_id, tag.text, tag['href'])

        # bulleted list
        elif tag.name == 'li':
            type = 'bulleted_list_item'
            n.add_text(page_id, type, tag.text)

        elif tag.name == 'blockquote':
            type = 'quote'
            n.add_text(page_id, type, tag.text)

        # mark -- background color
        elif tag.name == 'mark':
            annotations = {'color': 'orange_background'}
            n.add_text(page_id, 'paragraph', tag.text, annotations)

        # span -- bold
        elif tag.name == 'span':
            if tag.contents[0].name == 'mark':
                annotations = {'color': 'orange_background'}
                n.add_text(page_id, 'paragraph', tag.text, annotations)
            elif style == 'font-weight: bold;': # 仅判断了是否为粗体
                annotations = {'bold': True}
                n.add_text(page_id, 'paragraph', tag.text, annotations)
            else:
                n.add_text(page_id, 'paragraph', tag.text)

        return ''

def process_block(block_tag, paragraph, page_id):
    tags = block_tag.contents
    if len(tags) != 0:
        for tag in tags:
            paragraph = process_tag(tag, paragraph, page_id)
    return paragraph

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
    content = bs.find('div', class_='rich-content topic-richtext').contents # bs.find('div', {'class': 'rich-content topic-richtext'})
    content = content[1:-1]
    paragraph = ''
    for item in content:
        if item.name in ['p', 'div', 'span', 'ul']:
            paragraph = process_block(item, paragraph, page_id)
        else:
            paragraph = process_tag(item, paragraph, page_id)

    if paragraph:
        n.add_paragraph(page_id, paragraph)

    # divider
    n.add_simple_block(page_id, 'divider')

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

    n.add_paragraph(page_id, comm_paragraph)


if __name__ == '__main__':
    url = 'https://www.douban.com/group/topic/262187679/'
    db_id = '2c010a7238ff4802a45855c861e84d7d'
    crawl(url, db_id)

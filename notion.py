import requests
import logging
from utils import response_or_error


class Douban2Notion():
    def __init__(self, token):
        self.headers = {
            "Authorization": "Bearer " + token,
            "Notion-Version": "2022-02-22"
        }
        self.base_url = 'https://api.notion.com/v1'

    def search_page(self, page_title):
        body = {}
        if page_title is not None:
            body['query'] = page_title

        url = self.base_url + '/search'
        resp = requests.request('POST', url, headers=self.headers, json=body)
        return response_or_error(resp)

    def create_page(self, parent_id, title, author):
        '''
        specify the property name & type
        database? block?
        initial properties ...
        :param title:
        :return:
        '''
        body = {
            'parent': {'type': 'database_id', 'database_id': parent_id},
            'properties': {
                'Name': {
                    'title': [
                        {
                            'text': {
                                'content': title
                            }
                        }
                    ]
                },
                'Author': {
                    'rich_text': [
                        {
                            'type': 'text',
                            'text': {
                                'content': author
                            }
                        }
                    ]
                }
            }
        }
        resp = requests.request('POST', 'https://api.notion.com/v1/pages', json=body, headers=self.headers)
        return response_or_error(resp)


    # def update_page_properties(self, page_id, author):
    #     '''
    #     update property value
    #     other than page
    #     other than author
    #     :return:
    #     '''
    #     url = os.path.join(self.base_url, 'pages', page_id)
    #     body = {
    #         'properties': {
    #             'Author': {
    #                 'type': 'text',
    #                 'text': {
    #                     'content': author
    #                 }
    #             },
    #         }
    #     }
    #
    #     # for k, v in dct.items():
    #     #     case
    #
    #     resp = requests.request('PATCH', url, json=body, headers=self.headers)
    #     return resp.json()

    ## add-----------------------------------------
    def add_block(self, parent_id, children: []):
        '''
        basic function
        add: append block children
        :param parent_id:
        :param children:
        :return:
        '''
        url = self.base_url + f'/blocks/{parent_id}/children'
        resp = requests.request('PATCH', url, json={'children': children}, headers=self.headers)

        return response_or_error(resp)


    def add_image(self, parent_id, img_url):
        children = [
            {
                'type': 'image',
                'image': {
                    'type': 'external', # external
                    'external': {
                        'url': img_url
                    }
                }
            }
        ]
        resp = self.add_block(parent_id, children)
        return resp


    def add_text(self, parent_id, type, text, annotations=None):
        children = [
            {
                "type": type,
                type: {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": text,
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        }
                    }]
                },
            }
        ]
        if annotations:
            for k, v in annotations.items():
                try:
                    children[0][type]['rich_text'][0]['annotations'][k] = v
                except Exception as e:
                    logging.error(str(e)+f"No such key as '{k}' in annotations")
        resp = self.add_block(parent_id, children)
        return resp


    def add_paragraph(self, parent_id, paragraph):
        '''
        based on add_text, long paragraph
        :param parent_id:
        :param paragraph:
        :return:
        '''
        chunk_num = len(paragraph) // 1500 + 1
        for i in range(chunk_num):
            chunk = paragraph[1500 * i:1500 * (i + 1)]
            self.add_text(parent_id, 'paragraph', chunk)


    def add_link(self, parent_id, link_text, url):
        children = [
            {
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": link_text,
                            "link": {
                                'type': 'url',
                                'url': url
                            }
                        }
                    }],
                }
            }
        ]
        resp = self.add_block(parent_id, children)
        return resp


    def add_simple_block(self, parent_id, type):
        children = [
            {
                'object': 'block',
                'type': type,
                type: {}
            }
        ]
        resp = self.add_block(parent_id, children)
        return resp


    ## update-----------------------------------------
    def update_block(self, block_id, content: dict):
        '''
        basic function
        update: update a block
        :param block_id:
        :param content:
        :return:
        '''
        url = self.base_url + f'/blocks/{block_id}'
        resp = requests.request('PATCH', url, json=content, headers=self.headers)
        response_or_error(resp)


    def update_text(self, block_id, new_text: str):
        '''
        based on update_block
        :param block_id:
        :param text:
        :return:
        '''
        block = self.get_block(block_id)
        type = block['type']
        block[type]["text"][0]["text"]["content"] = new_text
        resp = self.update_block(block_id, block)
        response_or_error(resp)


    def get_block(self, block_id):
        pass


    def delete_block(self, block_id):
        url = self.base_url + f'/blocks/{block_id}'
        resp = requests.request('DELETE', url, headers = self.headers)
        response_or_error(resp)


# body = {
#             'properties': {
#                 'status': {
#                     'checkbox': True
#                 },
#                 'Tags': {
#                     'type': 'select',
#                     'select': {
#                         'name': '喜剧',
#                         'color': 'blue'
#                     }
#                 }
#             }
#         }

# children = {
#             "type": "paragraph",
#             "paragraph": {
#                 "rich_text": [{
#                     "type": "text",
#                     "text": {
#                         "content": content,
#                     }
#                 }],
#             }
#         }
# body = {'children': [children]}
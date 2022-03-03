import requests
import os
import logging

class Notion():
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
        resp = requests.request('POST', url, headers=headers, json=body)
        return resp.json() # 根据status_code作一些判断

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
        return resp.json()

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


    def update_page_content(self, page_id, content):
        '''
        other than page
        :return:
        '''
        url = f'https://api.notion.com/v1/blocks/{page_id}/children'
        children = {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": content,
                    }
                }],
            }
        }
        body = {'children': [children]}
        resp = requests.patch(url, json=body, headers=self.headers)

        if resp.status_code != 200:
            logging.error(resp.json()['message'])

    def add_block(self, page_id, type):
        '''
        no value
        :param page_id:
        :param type:
        :return:
        '''
        url = f'https://api.notion.com/v1/blocks/{page_id}/children'
        children = [
            {
                'object': 'block',
                'type': type,
                type: {}
            }
        ]
        body = {'children': children}
        resp = requests.patch(url, json=body, headers=self.headers)

        if resp.status_code != 200:
            logging.error(resp.json()['message'])


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
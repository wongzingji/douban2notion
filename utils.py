import logging

def response_or_error(resp):
    if resp.status_code == 200:
        return resp.json()
    else:
        # type = body[0]['type']
        # if type == 'paragraph':
        #     content = body[0]['paragraph']['rich_text']['text']['content']
        # else:
        #     content = ''
        # logging.error(type + ':' + content + '\n' + resp.json()['message'])
        logging.error(resp.json()['message'])
        return -1

import logging

def response_or_error(resp):
    if resp.status_code == 200:
        return resp.json()
    else:
        logging.error(resp.json()['message'])
        return -1

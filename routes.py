from utils import log

import random
import string

message_list = []
session = {}


def template(name):
    # windows 默认写的编码和打开的编码都是 'gbk' 编码,
    # 这里要指定 'utf-8' 编码
    path = 'templates/' + name
    log('path', path)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request, json_data):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    body = body.replace('{{json}}', json_data)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


route_dict = {
    '/': route_index,
}

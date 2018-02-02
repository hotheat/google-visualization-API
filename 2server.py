# coding: utf-8
"""
课 2 上课用品
2016.8.11

本次上课的主要内容有
0, 请注意代码的格式和规范
1, 规范化生成响应
2, HTTP 头
3, 几个常用 HTML 标签及其用法
4, 参数传递的两种方式

"""
# 下面这行注释是给 atom 的 pylint 用的, 忽略
# pylint: disable=C0103

import socket
import urllib.parse


from routes import route_dict
from utils import log
from gviz_data import get_gviz_data

# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def add_cookies(self):
        """
        Cookie: user=inivisivle
        :return:
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        log('cookie', kvs)
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

    def add_headers(self, header):
        """
        Accept-Encoding: gzip, deflate
        Cookie: user=inivisivle
        """
        for line in header:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        self.add_cookies()

    def form(self):
        # log('body before', self.body)
        body = urllib.parse.unquote(self.body)
        # log('body after', body)
        args = body.split('&')
        f = {}
        if not args == ['']:
            log('args', args)
            for arg in args:
                k, v = arg.split('=')
                f[k] = v
            log('f', f)
        return f



request = Request()
json_data = get_gviz_data()
log(json_data)

def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def parsed_path(path):
    """

    message=hello&author=gua
    {
        'message' : 'hello',
        'author' : 'gua',
    }

    :param path:
    :return:
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)
    response = route_dict.get(path, error)
    return response(request, json_data)


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        # 无限循环来处理请求
        while True:
            # 监听 接受 读取请求数据 解码成字符串
            s.listen(3)
            connection, address = s.accept()
            r = connection.recv(1024)
            r = r.decode('utf-8')
            log('ip and r, {}\n{}'.format(address, r))
            # try:
            # 因为 chrome 会发送空请求导致 split 得到空 list
            # 所以这里用 try 防止程序崩溃
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            request.method = r.split(' ')[0]
            # # 把 headers 放入 request 中
            request.add_headers(r.split('\r\n\r\n')[0].split('\r\n')[1:])
            # 把 body 放入 request 中
            request.body = r.split('\r\n\r\n', 1)[1]
            # log('request.body', request.body)
            # r_header_ls = r.split('\r\n')[1:3]
            # for i in r_header_ls:
            #     header_value = i.split(':')
            #     request.headers[header_value[0]] = header_value[1]
            # log('request headers', request.headers)
            # 用 response_for_path 函数来得到 path 对应的响应内容
            response = response_for_path(path)
            log('response', response)
            # 把响应发送给客户端
            connection.sendall(response)
            # except Exception as e:
            #     log('error', e)
            # 处理完请求, 关闭连接
            connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    # 如果不了解 **kwargs 的用法, 上过基础课的请复习函数, 新同学自行搜索
    run(**config)

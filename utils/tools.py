import socket
from json import dumps, JSONDecodeError, loads
from typing import Union

import httpx
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
from utils.root import get_project_root
from utils.terminal import color_wrap


"""
General FX.
"""


def print_req_obj(req: httpx.Request, res: Union[httpx.Response, None] = None, print_now: bool = False) -> str:
    if res:
        res.read()
        req = res.request
        http_ver = res.http_version
    else:
        http_ver = 'HTTP/1.1(Guess.)'
    req.read()
    req_str = f'{color_wrap(Fore.BLACK + str(req.method), Back.MAGENTA)} {req.url} {http_ver}\n'
    for key, val in req.headers.multi_items():
        req_str += f'{key.title()}: {val}\n'

    if req.content:
        try:
            req_str += f"Req Body (JSON): \n{color_wrap(Fore.BLUE + dumps(loads(req.read()), indent=4))}"
        except JSONDecodeError:
            req_str += f"Req Body (HTML): \n" \
                       f"{color_wrap(Fore.BLUE + BeautifulSoup(req.read().decode('utf-8'), 'lxml').prettify())}"
    req_str += '\n'
    if print_now:
        print(f'{Fore.LIGHTBLUE_EX}{req_str}{Style.RESET_ALL}')
    return req_str


def print_req_info(res: httpx.Response, print_headers: bool = False, print_body: bool = False):
    if not res:
        print('No Response Body')
        return

    with open(f'{get_project_root()}/src.html', mode='w', encoding='utf-8') as file:
        try:
            with open(f'{get_project_root()}/src.json', mode='w', encoding='utf-8') as js_file:
                js_file.write(dumps(res.json(), indent=4))
                # print('wrote json')
        except JSONDecodeError:
            file.write(res.text)
    if not print_headers:
        return

    req_str = print_req_obj(res.request, res)

    resp_str = f'{res.http_version} {color_wrap(Fore.BLACK + str(res.status_code), Back.MAGENTA)} {res.reason_phrase}\n'
    for key, val in res.headers.multi_items():
        resp_str += f'{key.title()}: {val}\n'
    resp_str += f'Cookie: '
    for key, val in res.cookies.items():
        resp_str += f'{key}={val};'
    resp_str += '\n'

    if print_body:
        try:
            resp_str += f"Resp Body (JSON): \n{color_wrap(Fore.BLUE + dumps(res.json(), indent=4))}"
        except JSONDecodeError:
            resp_str += f"Resp Body (HTML): \n{color_wrap(Fore.BLUE + BeautifulSoup(res.text, 'lxml').prettify())}"
    resp_str += '\n|\n|'

    sep_ = '-' * 10
    boundary = '|'
    boundary += '=' * 100
    print(boundary)
    print(f'|{sep_}REQUEST{sep_}')
    print(req_str)
    print(f'|{sep_}RESPONSE{sep_}')
    print(resp_str)
    print(f'|History: {res.history}')
    for resp in res.history:
        print(resp.url, end='\n')
    print()
    print(boundary)


def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port
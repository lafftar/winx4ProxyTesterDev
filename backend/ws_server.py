"""
This interfaces with the ws client active on the frontend to enable backend functions.
"""


async def check_proxy_format():
    """
    checks a list of proxies, returns the
        - number of ip auth
        - number of user/pass auth
        - number of http/s and socks4/5 proxies
    as well as any formats that are not recognized
    :return:
    """
    pass
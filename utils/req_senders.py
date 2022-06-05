import asyncio
import ssl
from asyncio import sleep

import aiohttp
import anyio
import httpx
from aiohttp import client_exceptions

from utils.custom_logger import Log

log = Log('[REQ SENDER]')


async def httpx_send_req(req: httpx.Request, client: httpx.AsyncClient, num_tries: int = 5) -> \
        httpx.Response | aiohttp.ClientResponse | None:
    """
    Central Request Handler. All requests should go through this.
    :param client:
    :param req:
    :param num_tries:
    :return:
    """
    for _ in range(num_tries):
        try:
            item = await client.send(req)
            return item
        except (
                # httpx errors
                httpx.ConnectTimeout, httpx.ProxyError, httpx.ConnectError,
                httpx.ReadError, httpx.ReadTimeout, httpx.WriteTimeout, httpx.RemoteProtocolError,

                # ssl errors
                ssl.SSLError,

                # aiohttp errors
                asyncio.exceptions.TimeoutError, client_exceptions.ClientHttpProxyError,
                client_exceptions.ClientProxyConnectionError,
                client_exceptions.ClientOSError,
                client_exceptions.ServerDisconnectedError,

                # any io errors
                anyio.ClosedResourceError
        ) as c:
            await sleep(2)
    return


if __name__ == "__main__":
    pass

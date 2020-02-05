#
# asyhttp.py
# ----------
# author: ax
# author: pyno
#
# This is asyhttp, a simple module to perform async HTTP requests using asyncio and aiohttp.
# It provides a trivial way to perform a set of async HTTP requests.
#
#

import asyncio
from aiohttp import ClientSession, TCPConnector, client_exceptions
from aiohttp_proxy import ProxyConnector, ProxyType
import sys

version = "0.2"

def loop(urls, process_out=None, proxy='', verify_tls=False, redirects=False, max_concurrent=1000, usrdata={}):
    if len(urls) < 1:
        sys.stdout.write(" [!] No URL list in loop.\n [!] Bye!\n")
        exit(1)
    if process_out:
        process_output = process_out
    else:
        def process_output(url,return_code,reason,resp_body,usr_data):
            sys.stdout.write(" [>] "+str(return_code)+" : "+url+"\n")
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_run_tasks(urls, proxy, max_concurrent, process_output, verify_tls, redirects, usrdata))
    except client_exceptions.ServerDisconnectedError as e:
        print("\n [!] Error ServerDisconnectedError - try lowering max_concurrent value")

async def _run_tasks(req_dict_list, proxy_str, max_concurrent, process_output, verify_tls, redirects, usrdata):
    tasks = []
    sem = asyncio.Semaphore(max_concurrent)

    conn = None
    if proxy_str != '':
        # ============== handle remote dns resolution =======================
        p = int(proxy_str.split(':')[2])
        h = proxy_str.split('://')[1].split(':')[0]
        conn = ProxyConnector(proxy_type=ProxyType.HTTP, host=h, port=p, rdns=True)
    else:
        conn = TCPConnector(ttl_dns_cache=None) # Number of secs, None means cached forever

    async with ClientSession(connector=conn) as client:
        for req_dict in req_dict_list:
            # pyhton 3.7
            # tasks.append(asyncio.create_task(_bound_fetch(...)))
            # -----------------
            # tasks.append(asyncio.ensure_future(_bound_fetch(...)))
            tasks.append(_bound_fetch(sem,req_dict, client, process_output, verify_tls, redirects, usrdata))
        await asyncio.gather(*tasks)

async def _bound_fetch(sem, req_dict, client, process_output,verify_tls, redirects, usrdata):
    async with sem:
        await _fetch(req_dict,client,process_output,verify_tls,redirects,usrdata)

async def _fetch(req_dict,client,process_output,verify_tls,redirects,usrdata):
    if not "method" in req_dict:
        sys.stdout.write(" [!] Missing method in URL dict: {}\n".format(req_dict))
        return
    elif not "url" in req_dict:
        sys.stdout.write(" [!] Missing url in URL dict: {}\n".format(req_dict))
        return

    headers = {}
    if "headers" in req_dict:
        headers = req_dict["headers"]

    if req_dict["method"] == "GET":
        resp_body,return_code,reason = await _aGET(req_dict["url"],headers,client,verify_tls,redirects)
    elif req_dict["method"] == "HEAD":
        resp_body,return_code,reason = await _aHEAD(req_dict["url"],headers,client,verify_tls,redirects)
    elif req_dict["method"] == "POST":
        resp_body,return_code,reason = await _aPOST(req_dict["url"],headers,req_dict["body"],client,verify_tls,redirects)
    else:
        sys.stdout.write(" [!] HTTP method not supported: {}\n".format(req_dict["method"]))
        return
    process_output(req_dict["url"], return_code, reason, resp_body, usrdata)

async def _aGET(url,headers,client,verify_tls,redirects):
    async with client.get(url, headers=headers, verify_ssl=verify_tls, allow_redirects=redirects) as response:
        return_code = response.status
        reason = response.reason
        return await response.content.read(),return_code,reason

async def _aPOST(url,headers,body,client,verify_tls,redirects):
    async with client.post(url, headers=headers, data=body, verify_ssl=verify_tls, allow_redirects=redirects) as response:
        return_code = response.status
        reason = response.reason
        return await response.content.read(),return_code,reason

async def _aHEAD(url,headers,client,verify_tls,redirects):
    async with client.head(url, headers=headers, verify_ssl=verify_tls, allow_redirects=redirects) as response:
        return_code = response.status
        reason = response.reason
        return await response.content.read(),return_code,reason

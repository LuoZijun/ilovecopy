#!/usr/bin/env python3
#coding: utf8

import os
import functools
import base64
import asyncio

import aiohttp.web


"""
JS Code:

let canvas;
let bpng;
let xhr;

canvas = $('canvas')[0];
bpng = canvas.toDataURL("image/png").replace("data:image/png;base64,", "");

xhr = new XMLHttpRequest();
xhr.open('POST', 'http://127.0.0.1:8080', true);
xhr.send(bpng);

"""


async def index(req):
    content = await req.content.read()
    buff = content.decode("UTF-8").replace("data:image/png;base64,", "").encode("UTF-8")
    png = base64.decodebytes(buff)
    open("img.png", "wb").write(png)
    await asyncio.sleep(2)
    print("IMAGE Length: %d" % len(png))
    print(req)
    return aiohttp.web.Response(text='')


def run_server():
    app = aiohttp.web.Application()
    app.router.add_post('/', index)

    aiohttp.web.run_app(app, host='127.0.0.1', port=8080)    

MACINTOSH_MOZILLA_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
LINUX_MOZILLA_AGENT     = 'Mozilla/5.0 (X11; Linux i686 on x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'
WINDOWS_MOZILLA_AGENT   = 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0'
GOOGLE_BOT_AGENT        = 'Googlebot/2.1 (+http://www.google.com/bot.html)'

HEADERS = {
    'User-Agent': MACINTOSH_MOZILLA_AGENT,
    'Referer': 'http://www.kubo720.com/case360/qianlijiangshantu/index.html',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate'
}

async def fetch(url):
    fname = os.path.join('data', url.split('/')[-1])
    if not os.path.exists('data'):
        os.mkdir('data')
    if os.path.exists(fname) and os.path.isfile(fname):
        await asyncio.sleep(0.1)
        print("[CACHE]: %s" % url)
        return True
    try:
        async with aiohttp.ClientSession(conn_timeout=30, read_timeout=30) as session:
            async with session.get(url, headers=HEADERS) as response:
                content = await response.content.read()
                open(fname, "wb").write(content)
                print("[DOWNLOAD]: %s" % url)
                return True
    except Exception as e:
        print("[ERROR]: %s \t %r" % (url, e) )
    return False

def worker():
    loop = asyncio.get_event_loop()
    urlbase = "http://www.kubo720.com/case360/qianlijiangshantu/panos/s01.tiles/l5/1/l5_1_%d.jpg"
    for n in range(60):
        jobs = list(map(lambda n: fetch(urlbase % n), range(n*5, n*5+5)))
        status = loop.run_until_complete(asyncio.gather(*jobs))
        print(status)


def main():
    # run_server()
    worker()

if __name__ == '__main__':
    main()




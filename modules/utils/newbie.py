import re

import aiohttp
import ujson as json

from core.dirty_check import check
from modules.wiki.wikilib import wikilib


async def newbie(wiki_url):
    pageurl = await wikilib().get_article_path(wiki_url) + 'Special:Log?type=newusers'
    if wiki_url:
        url = wiki_url + '?action=query&list=logevents&letype=newusers&format=json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=20)) as req:
            if req.status != 200:
                return f"请求时发生错误：{req.status}\n错误汇报地址：https://github.com/Teahouse-Studios/bot/issues/new?assignees=OasisAkari&labels=bug&template=5678.md&title="
            else:
                text1 = await req.text()
    file = json.loads(text1)
    d = []
    for x in file['query']['logevents']:
        d.append(x['title'])
    print(str(d))
    m = '\n'.join(d)
    y = await check(m)
    print(str(y))
    f = re.findall(r'.*\n.*\n.*\n.*\n.*', str(y))
    g = pageurl + '\n' + f[0] + '\n...仅显示前5条内容'
    if g.find('<吃掉了>') != -1 or g.find('<全部吃掉了>') != -1:
        return g + '\n检测到外来信息介入，请前往日志查看所有消息。Special:日志?type=newusers'
    else:
        return g

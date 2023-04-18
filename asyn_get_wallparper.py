import aiohttp
import asyncio
import aiofiles
from jsonpath_ng import parse


# 获取json数据并解析
async def get_json_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as req:
            temp_json = await req.json()
            temp_jsonpath = parse('$..fankitList[*].wallpaper.l')
            data = [match.value for match in temp_jsonpath.find(temp_json)]
            return data


# 获取图片url并下载图片
async def imgs_operation(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as req:
            filename = url.split("/")[-1] + '.jpg'
            content = await req.content.read()
            async with aiofiles.open(f'./imgs/{filename}', mode='wb') as fp:
                await fp.write(content)


async def main():
    base_url = 'https://www.arknights.global:8082/fankit/queryFankit?pageIndex=1&pageNum=999&type=1'
    data = await get_json_data(base_url)
    for url in data:
        img_url = 'https://webusstatic.yo-star.com/' + url
        print(img_url)
        await imgs_operation(img_url)


asyncio.run(main())

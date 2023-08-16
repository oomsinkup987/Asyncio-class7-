# https://flask.palletsprojects.com/en/2.3.x/
# https://www.python-httpx.org/async/
# https://flask.palletsprojects.com/en/2.3.x/quickstart/#rendering-templates

import asyncio
import time
from random import randint
import httpx
from flask import Flask, render_template

app = Flask(__name__)

# function converted to coroutine
async def get_xkcd_image(session:httpx.AsyncClient): # dont wait for the response of API
    comicid = randint(0 , 1000)
    response = await session.get(f'https://xkcd.com/{comicid}/info.0.json')
    return response.json()['img']

# function converted to coroutine
async def get_multiple_images(number):     
    async with httpx.AsyncClient as session:
        tasks = [get_xkcd_image(session, _ +1) for _ in range(number)]
        _ = await asyncio.gather(*tasks)
        return _


@app.get('/comic')
def hello():
    start  = time.perf_counter()
    urls = get_multiple_images(10)
    end = time.perf_counter()
    return render_template('index.html', end=end, start=start, urls = urls)

if __name__ == '__main__':
    app.run(debug=True, port=5555)

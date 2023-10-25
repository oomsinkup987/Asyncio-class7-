# https://flask.palletsprojects.com/en/2.3.x/
# https://www.python-httpx.org/async/
# https://flask.palletsprojects.com/en/2.3.x/quickstart/#rendering-templates

import asyncio
import time
from random import randint
import httpx
from flask import Flask, render_template

import asyncio
import time
from random import randint
import httpx
from flask import Flask, render_template


app = Flask(__name__)

# function converted to coroutine


async def get_xkcd_image(session):
    comcid = randint(0, 1000)
    response = await session.get(f'https://xkcd.com/{comcid}/info.0.json')
    return response.json()['img']

# function converted to coroutine


async def get_multiple_images(number):
    async with httpx.AsyncClient() as session:  # async client used for async functions
        tasks = [get_xkcd_image(session) for _ in range(number)]
        # gather used to collect all coroutines and run them using loop and get the ordered response
        result = await asyncio.gather(*tasks, return_exceptions=True)
    return result


@app.get('/comic')
async def hello():
    start = time.perf_counter()
    urls = await get_multiple_images(100)
    end = time.perf_counter()
    return render_template('index.html', end=end, start=start, urls=urls)


if __name__ == '__main__':
    app.run(debug=True, port=5555)
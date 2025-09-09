#!/usr/bin/env python3
#
# pjsk bot

from asyncio import run
from os import environ
from telebot.async_telebot import AsyncTeleBot
from aiohttp import ClientSession
from orjson import loads

bot = AsyncTeleBot(environ["TOKEN"])

@bot.message_handler(commands=["b"])
async def leaderboard(message):
    args = message.text.split()
    region = args[1]
    evtype = args[2]
    page = args[3]
    if evtype == "wl":
        type = "live_latest_chapter"
    elif evtype == "nowl":
        type = "live"
    url = f"https://api.sekai.best/event/{type}?region={region}"
    if page == "1":
        tops = range(0, 51)
    elif page == "2":
        tops = range(50, 103)
    raw = await sget(url)
    json = loads(raw)
    data = json["data"]["eventRankings"]
    result = "".join(f"{data[top]['rank']}  {data[top]['userName'][:20]}"
                     + f"  {data[top]['score']}\n" for top in tops)
    await reply(message, result)

async def reply(message, result):
    await bot.reply_to(message, result)

async def sget(url):
    headers = ({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                + "AppleWebKit/537.36 (KHTML, like Gecko)"
                + "Chrome/100.0.4896.127 Safari/537.36"})
    async with ClientSession() as s:
        async with s.get(url, headers=headers) as resp:
            return await resp.text()

run(bot.infinity_polling())

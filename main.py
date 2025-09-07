#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
from asyncio import run
from os import environ
from telebot.async_telebot import AsyncTeleBot
from aiohttp import ClientSession
from orjson import loads

bot = AsyncTeleBot(environ['TOKEN'])


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    async def leaderboard(
    ctx: Interaction,
    page: int = SlashOption(choices=[1, 2], description="page = 50 tiers"),
    region: str = SlashOption(choices=["en", "kr", "jp", "tw", "cn"]),
    wl: bool = SlashOption(choices=[True, False]),
):
    if wl:
        type = "live_latest_chapter"
    else:
        type = "live"
    url = f"https://api.sekai.best/event/{type}?region={region}"
    if page == 1:
        tops = range(0, 51)
    elif page == 2:
        tops = range(50, 103)
    raw = await sget(url)
    json = loads(raw)
    data = json["data"]["eventRankings"]
    leaderboard = "".join(f"{data[top]['rank']}  {data[top]['userName'][:20]}"
                          + f"  {data[top]['score']}\n" for top in tops)
    result = "```\n" + leaderboard + "```"
    await reply(ctx, result)
    await bot.reply_to(message, text)


async def sget(url):
    headers = ({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                + "AppleWebKit/537.36 (KHTML, like Gecko)"
                + "Chrome/100.0.4896.127 Safari/537.36"})
    async with ClientSession() as s:
        async with s.get(url, headers=headers) as resp:
            return await resp.text()

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)


run(bot.infinity_polling())

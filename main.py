import asyncio
import discord
import requests
import random
from discord.ext import commands
with open("token.txt", "r") as tf:
    TOKEN_LIST = tf.readlines()
TOKEN = "".join(map(str.strip, TOKEN_LIST))
dashes = (1,2,3,4,5,6)

Bot = commands.Bot(command_prefix="!")

WEATHER_API_KEY = "dc972cf9-8a9d-49ca-acca-bdf6f98dc450"
headers = {"X-Yandex-API-Key":WEATHER_API_KEY}

def get_coords(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        return toponym_coodrinates.split(" ")
    else:
        return None, None

def weather_response(place):
    coords = ("39.954987", "43.412182")
    coords = get_coords(place)
    print("Погода в ", place, coords)
    weather_api_server = "https://api.weather.yandex.ru/v1/forecast?"
    weather_param =  {
        "lon":float(coords[0]),
        "lat":float(coords[1]),
        "lang":"ru_RU"
    }
    responce = requests.get(weather_api_server, weather_param, headers=headers)
    return responce.json()

def current_weather(response):
    city = response["info"]["tzinfo"]["name"].split('/')[-1]
    date = response["now_dt"][:10]
    offset = response["info"]["tzinfo"]["offset"] // 3600
    time = response["now_dt"][11:16]
    h, m = map(int, time.split(':'))
    time = f'{h + offset}:{m:02}'
    fact = response["fact"]
    temp = fact["temp"]
    condition = fact["condition"]
    wind_dir = fact["wind_dir"]
    wind_speed = fact["wind_speed"]
    pressure = fact["pressure_mm"]
    humidity = fact["humidity"]
    return f'Current weather in {city} today {date} at time {time}:\n' \
           f'Temperature: {temp},\n' \
           f'Pressure: {pressure} mm,\n' \
           f'Humidity: {humidity}%,\n' \
           f'{condition},\n' \
           f'Wind {wind_dir}, {wind_speed} m/s.'


@Bot.event
async def on_ready():
   print(f'{Bot.user} подключен к Discord!')
   for guild in Bot.guilds:
       print(
           f'{Bot.user} подключились к чату:\n'
           f'{guild.name}(id: {guild.id})'
       )

@Bot.command(pass_context=True)
async def hello(ctx):
    await ctx.send("Привет Hello Gracias")

@Bot.command(name='roll_dice')
async def roll_dice(self, ctx, count):
    res = [random.choice(dashes) for _ in range(int(count))]
    await ctx.send(" ".join(res))

@Bot.command(name="current")
async def current(ctx):
    response = weather_response("Сочи")
    message = current_weather(response)
    await ctx.send(message)
@Bot.command()
async def Ti_lox(ctx):
    await ctx.send("Ах ты собака дурак идиот да чтоб ты сгорел говно")
@Bot.command(name="randint")
async def my_randint(ctx, min_int, max_int):
    num = random.randint(int(min_int), int(max_int))
    await ctx.send(num)
Bot.run(TOKEN)
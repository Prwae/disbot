import asyncio
import discord
import random
from discord.ext import commands
with open("token.txt", "r") as tf:
    TOKEN = tf.readline()

#client = discord.Client()
Bot = commands.Bot(command_prefix="!")
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

@Bot.command()
async def Ti_lox(ctx):
    await ctx.send("Ах ты собака дурак идиот да чтоб ты сгорел говно собачье")
@Bot.command(name="randint")
async def my_randint(ctx, min_int, max_int):
    num = random.randint(int(min_int), int(max_int))
    await ctx.send(num)
Bot.run(TOKEN)
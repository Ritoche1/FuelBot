#!/usr/bin/env python3

import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_ui import Components, Button, UI, ButtonInteraction
import json
import requests

from town import Town
from tools import getEmbedPage, downloadFile, getDataFromId, isUpdated

message = []

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)
ui = UI(bot)

data = json.load(open("config.json"))

@bot.event
async def on_ready():
    print("Bot is ready!")

@slash.slash(name="search", description="Make a research of the price in the town")
async def _search(ctx: SlashContext, ville: str):
    ville = ville.lower()
    town = Town()
    town.classFindTown(ville)
    if town.town != []:
        embed = getEmbedPage(town, 0)
        button1 = Button(label="Previous", emoji="⬅", custom_id="previous")
        button2 = Button(label="Next", emoji="➡", custom_id="next")
        tmp = await ctx.send(embed=embed)
        button = await ui.components.send(ctx.channel,components=[button1, button2])
        message.append({
            "message": tmp.id,
            "button": button.id,
            "town" : town
        })
    else:
        await ctx.send(content="La ville n'a pas été trouvée")


@slash.slash(name="cheapest", description="Make a research of the cheapest price near the town")
async def _cheap(ctx: SlashContext, ville: str, distance : int):
    ville = ville.lower()
    town = Town()
    town.classFindNearCheap(ville, distance)
    if town.town != []:
        embed = getEmbedPage(town, 0)
        # await ctx.send(embeds=[embed])
        button1 = Button(label="Previous", emoji="⬅", custom_id="previous")
        button2 = Button(label="Next", emoji="➡", custom_id="next")
        tmp = await ctx.send(embed=embed)
        button = await ui.components.send(ctx.channel,components=[button1, button2])
        message.append({
            "message": tmp.id,
            "button": button.id,
            "town" : town
        })
    else:
        await ctx.send(content="La ville n'a pas été trouvée")



@slash.slash(name="update", description="Update the fuel file")
async def _update(ctx: SlashContext):
    if (isUpdated()):
        await ctx.send(content="Le fichier est déjà à jour")
    elif (ctx.author.id == data['OWNER']):
        await ctx.send(content="Mise à jour du fichier...")
        await downloadFile()
        await ctx.send(content="Fichier mis à jour")
    else :
        await ctx.send(content="Vous n'avez pas les droits pour cette commande, demandez à l'admin")


@bot.listen("on_button")
async def on_button(btn: ButtonInteraction):
    custom_id = btn.data['custom_id']
    town, idButton, idMessage = getDataFromId(message, btn.message.id)
    tmp_message = await bot.get_channel(btn.channel_id).fetch_message(idMessage)
    if custom_id == "previous":
        if (town.page - 1) >= 0:
            town.setPage(town.getPage() - 1)
            embed = getEmbedPage(town, town.getPage())
            await tmp_message.edit(embed=embed)
        else:
            town.setPage(len(town.town))
            embed = getEmbedPage(town, town.getPage())
            await tmp_message.edit(embed=embed)
    elif custom_id == "next":
        if (town.page + 1) < len(town.town):
            town.setPage(town.getPage() + 1)
            embed = getEmbedPage(town, town.getPage())
            await tmp_message.edit(embed=embed)
        else:
            town.setPage(0)
            embed = getEmbedPage(town, town.getPage())
            await tmp_message.edit(embed=embed)
    await btn.respond(ninja_mode=True)
            

bot.run(data['TOKEN'])

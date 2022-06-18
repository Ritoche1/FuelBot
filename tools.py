#!/usr/bin/env python3

import requests
import json
import discord


class Tools:
    def __init__(self, town):
        self.town = []
        self.address = []
        self.cp = []
        self.geom = []
        self.price = []
        self.gas = []
        self.date = []
        self.classFindTown(town)
        self.page = 0

    def classFindTown(self, city):
        town = findTown(city)
        if town != None:
            for i in town:
                self.town.append(i['ville'])
                self.address.append(i['adresse'])
                self.cp.append(i['cp'])
                self.geom.append(i['geom'])
                self.price.append(i['prix_valeur'])
                self.gas.append(i['prix_nom'])
                self.date.append(i['prix_maj'])

            # self.town = town['ville']
            # self.address = town['adresse']
            # self.cp = town['cp']
            # self.geom = town['geom']
            # self.price = town['prix_valeur']
            # self.gas = town['prix_nom']
            # self.date = town['prix_maj']
    def setPage(self, page):
        self.page = page
    def getPage(self):
        return self.page


def getEmbedPage(town : Tools, i):
    embed = discord.Embed(title=town.town[i], color=0xc2dd2c, description="Page " + str(i + 1) + "/" + str(len(town.town)))
    embed.add_field(name="Adresse", value=town.address[i], inline=False)
    embed.add_field(name="Code Postale", value=town.cp[i], inline=False)
    embed.add_field(name="Prix", value=str(town.price[i]) + "€/L")
    embed.add_field(name="Type", value=town.gas[i])
    embed.set_footer(text="Mise à jour le " + town.date[i])
    return embed


async def downloadFile():
    Url = "https://www.data.gouv.fr/fr/datasets/r/b3393fc7-1bee-42fb-a351-d7aedf5d5ff0"
    r = requests.get(Url, allow_redirects=True)
    open('dataEssence.json', 'wb').write(r.content)
    print("Fichier mis à jour")

def findTown(town):
    res = []
    with open('dataEssence.json', 'r') as f:
        data = json.load(f)
        for i in data:
            if i['fields']['ville'] == town:
                res.append(i['fields'])
    if len(res) == 0:
        return None
    return res

def getDataFromId(message, id):
    for i in message:
        if (i['button'] == id):
            return i['town'], i['button']
    return None
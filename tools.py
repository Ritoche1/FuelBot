#!/usr/bin/env python3

from datetime import datetime
import requests
import json
import discord


def getEmbedPage(town, i):
    URL = f"https://www.google.fr/maps/place/{town.address[i].replace(' ', '+')}+{town.cp[i]}"
    embed = discord.Embed(title=town.town[i], color=0xc2dd2c, description="Page " + str(i + 1) + "/" + str(len(town.town)), url=URL)
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
    try :
        with open('dataEssence.json', 'r') as f:
            data = json.load(f)
            for i in data:
                if i['fields']['ville'].lower() == town:
                    res.append(i['fields'])
    except FileNotFoundError:
        print("Fichier non trouvé")
    if len(res) == 0:
        return None
    return res

def getTownGeom(town):
    try :
        with open('dataEssence.json', 'r') as f:
            data = json.load(f)
            for i in data:
                if i['fields']['ville'].lower() == town:
                    return i['fields']['geom']
    except FileNotFoundError:
        print("Fichier non trouvé")
    return None

def findNearCheap(town, distance):
    res = []
    geom = getTownGeom(town)
    try :
        with open('dataEssence.json', 'r') as f:
            data = json.load(f)
            for i in data:
                if getDistance(i['fields']['geom'], geom) < distance:
                    res.append(i['fields'])
        return (getCheapest(res))
    except FileNotFoundError:
        print("Fichier non trouvé")

def isTypeInIt(type, list):
    for i in list:
        if i['prix_nom'] == type:
            return True
    return False

def getCheapest(res):
    near = []
    found = 0
    for station in res:
        found = 0
        for i in near :
            try :
                if i['prix_valeur'] > station['prix_valeur'] and i['prix_nom'] == station['prix_nom'] and datetime.strptime(station["prix_maj"],"%Y-%m-%dT%H:%M:%S+02:00").date() == datetime.now().date():
                    found = 1
                    near.remove(i)
                elif not isTypeInIt(station['prix_nom'], near) and datetime.strptime(station["prix_maj"],"%Y-%m-%dT%H:%M:%S+02:00").date() == datetime.now().date():
                    found = 1
            except KeyError:
                break
        if near == [] or found == 1 and datetime.strptime(station["prix_maj"],"%Y-%m-%dT%H:%M:%S+02:00").date() == datetime.now().date():
            near.append(station)
    if len(res) == 0:
        return None
    return (near)

def getDataFromId(message, id):
    for i in message:
        if (i['button'] == id):
            return i['town'], i['button'], i['message']
    return None

def getDistance(first, second):
    distance = (abs((first[0] - second[0])) + abs((first[1] - second[1]))) * 69.0
    return distance

def isUpdated():
    try :
        with open('dataEssence.json', 'r') as f:
            data = json.load(f)
            for i in data:
                if datetime.strptime(i['fields']['prix_maj'],"%Y-%m-%dT%H:%M:%S+02:00").date() == datetime.now().date():
                    return True
    except FileNotFoundError:
        print("Fichier non trouvé")
    return False

if __name__ == "__main__":
    res = findNearCheap("Lille", 5)
#!/usr/bin/env python3

from tools import findNearCheap, findTown

class Town:
    def __init__(self):
        self.town = []
        self.address = []
        self.cp = []
        self.geom = []
        self.price = []
        self.gas = []
        self.date = []
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
    def classFindNearCheap(self, city, distance):
        town = findNearCheap(city, distance)
        if town != None:
            for i in town:
                self.town.append(i['ville'])
                self.address.append(i['adresse'])
                self.cp.append(i['cp'])
                self.geom.append(i['geom'])
                self.price.append(i['prix_valeur'])
                self.gas.append(i['prix_nom'])
                self.date.append(i['prix_maj'])
    def setPage(self, page):
        self.page = page
    def getPage(self):
        return self.page

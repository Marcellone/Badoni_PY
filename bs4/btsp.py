#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

urlBadoni = "https://www.iisbadoni.edu.it/categoria/circolari"
req = requests.get(urlBadoni)
soup = BeautifulSoup(req.text, "lxml")

itemsList = soup.find("div", {"class": "view-content"})


for item in itemsList.find_all("div", {"class": "views-row"}):
    titolo = item.find("a")
    if titolo:
        titolo = titolo.text
        if titolo != "Leggi tutto ...":
            print(titolo)

    sommario = item.find("p").text

    print(sommario)

    dataEmissione = item.find("span", {"class": "views-field-created"})
    dataEmissione = dataEmissione.find("span", {"class": "field-content"})
    print(dataEmissione.text)
    print("\n\n")

#!/usr/bin/env python

import requests
import time
from bs4 import BeautifulSoup
from discord_webhooks import DiscordWebhooks
webhook=DiscordWebhooks("https://discord.com/api/webhooks/760050656542326785/rDFVNuo953TiTgWSqTeJG12NiggjiFjwmb7ukP6CjEApa73qCW6BEJLsgrOPLy65cAmV")

while True:

    with open("lastEntry.txt", "r") as f:
        lastEntry = f.read()
    isLast = False

    urlBadoni = "https://www.iisbadoni.edu.it/categoria/circolari"
    req = requests.get(urlBadoni)
    soup = BeautifulSoup(req.text, "lxml")

    itemsList = soup.find("div", {"class": "view-content"})
    circolari = []

    for item in itemsList.find_all("div", {"class": "views-row"}):
        for head in item.find_all("a"):
            if head:
                if head.text != "Leggi tutto ...":
                    titolo = head.text
        
                elif head.text == "Leggi tutto ...":
                    link = "https://www.iisbadoni.edu.it/" + head["href"]

        sommario = item.find("p").text
        dataEmissione = item.find("span", {"class": "views-field-created"})
        dataEmissione = dataEmissione.find("span", {"class": "field-content"}).text

        circolari.append({"titolo": titolo,
                          "sommario": sommario,
                          "data": dataEmissione,
                          "url": link})

    for item in circolari:
        if item["titolo"] == lastEntry:
            print("non ci sono circolari")
            isLast = True


        if not isLast:
            print(item)
            webhook.set_content(title=item["titolo"],
                                description=item["sommario"]+"\nData: "+item["data"],
                                url=item["url"],
                                color=0xFF0000)
            webhook.set_author(name="Nuova circolare")
            webhook.set_footer(text="Badoni circolari")
            webhook.send()   
            print("webhook inviato")
            print("\n\n")
            time.sleep(1)

    with open("lastEntry.txt", "w+") as f:
        f.write(circolari[0]["titolo"])
    time.sleep(240) 

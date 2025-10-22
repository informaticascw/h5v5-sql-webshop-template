# h5v5-sql-webshop-template
Startcode voor het programmeren van een webshop met een html front end en python en database backend met rest api

Deze repo is onderdeel van het vak informatica op het Stanislascollege Westplantsoen.

Meer info over deze opdracht op<br>
[https://stanislas.informatica.nu/webshop/](https://stanislas.informatica.nu/webshop/)

## Snel bekijken?

Open een codespace

Start de webshop in de terminal van de codespace met het commando 
```
bash start.sh
```


# Tips hoe je de webshop kunt aanpassen 

## Server opnieuw starten
Gebruik het terminal window van je codespace.<br>
Stop de server door typen van [CRTL]+[C].<br>
Start de server met het volgene commando.<br>
```
bash start.sh
```

## Wijzigingen aanbrengen in de database
Wijzig de sql-commando's in het bestand `data/init.sql`<br>
Start de server opnieuw (zie elders hoe dat moet) nadat de sql-commando's gewijzigd zijn. Zo zorg je ervoor dat de database opnieuw gemaakt wordt door de nieuwe sql-commando's uit te voeren.

## Fouten zoeken in de database
Open de database in de terminal met het volgende commando
```
sqlite3 data/products.db
```
Je kunt met SQL commanda's zien wat er in de database staat.<br>
Bijvoorbeeld het commando: `SELECT * from Products;` (vergeet de puntkomma aan het einde niet)

Meer handige commando's:<br>
- Een lijstje met tabellen `.tables`
- De namen van de kolommen in de tabel products: `.schema products`
- De eerste 3 rijen van de tabel products: `SELECT * FROM products LIMIT 3;`
- sqlite3 afsluiten: `.quit`

Alle commando's:<br>
- https://www.sqlite.org/cli.html

## Fouten zoeken in de api
Je kunt het antwoord van de api testen door achter de link naar je webshop /api/products te typen, bijvoorbeeld:<br>
`https://....-8000.app.github.dev/api/products`<br> (pas .... aan voor jouw webshop-adres)

Bekijk de terminal van de server (dat is de terminal in je codespace), daar kun je foutmeldingen zien.
Je kunt in de code in de map api opdrachten toevoegen die inhoud van variabelen afdrukken. Bijvoorbeeld:
```
print("Waarde van i is ", i);
```
Start de server opnieuw (zie elders hoe dat moet) nadat de code gewijzigd is.

## Fouten zoeken in de webpagina's op de client
Bekijk de console in de browser, daar kun je foutmeldingen zien.<br>
In Chrome open je de console in het menu -> Weergave -> Ontwikkelaar -> JavaScript-console. <br>
Je kunt in de code op strategische plaatsen de volgende opdracht toevoegen:
```
debugger
```
Als de console open staat dan stopt de browser met het uitvoeren van code als hij het debugger commando tegenkomt. Je kunt dan via de console opdrachten geven. Je kunt de inhoud van variabelen bekijken met de opdracht:
```
console.log("Waarde van i is ", i);
```

# Uitleg over bestanden en mappen

## app/
`main.py` is het python programma dat de webserver voor de api en statische bestanden start.

## data/
Database met informatie over de artikelen in de webshop. De commando's in het `init.sql`-bestand zetten de informatie in de database. De database database wordt elke keer dat `bash start.sh` wordt uitgevoerd opnieuw gemaakt.

## static/
.html, .css en .js-bestanden die door de browser van de bezoeker van je webshop geladen worden. Ze vormen het raamwerk van hoe je webshop eruit ziet.<br>
In de submap `images/` staan plaatjes van je artikelen.

## start.sh
Dit bestand bevat de commando's om de webshop (opnieuw) te starten. Je voert dit bestand uit in de terminal met het commando
```
bash start.sh
```

## .devcontainer/
Mappen met de configuratie voor codespaces

## .vscode/
Map met de configuratie voor de editor VS Code die wordt gebruikt door codespaces

# Vraag en antwoord

## Codespace meldt "Oh no, it looks like you're offline"
Op sommige scholen blokkeert de firewall het gebruik van Codespaces. Dit is een instelling die alleen door de firewall beheerder kan worden aangepast. Tijdelijke oplossing: Verbind via een hotspot van je mobiel.

# Credits
- avs123a<br>
for a "Simple inventory list example with crud using : NodeJS, express framework, pug template, sqlite database and bootstrap". See https://github.com/avs123a/NodeJS-simple-example
- Robert Bakker [Notalifeform](https://www.gihub.com/Notalifeform)<br>
for help almost 24x7 with many questions and problems and providing basic shop called gitpodnode to be further developed by students on gitpod and deplyed freely on heroku. See https://gitpod.io/#https://github.com/Notalifeform/gitpodnode
- chatgpt for help converting the original idea (based on nodejs) to this idea (based on python)


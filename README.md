# db abfahrten

zeigt die abfahrten an einer haltestelle an, die im db navigator gelistet ist.

---

## config

die station id kriegt man am besten [hier](https://petstore.swagger.io/?url=https%3A%2F%2Fv6.db.transport.rest%2F.well-known%2Fservice-desc%0A#/default/get_locations), da dann einfach den namen suchen wie im db navigator und dann ist das `id` feld die station id.

in der config ist `direction_overrides` dafür da ggf. zu lange endhaltestellennamen sinnvoll zu kürzen, damit nicht einfach immer nach X positionen abgeschnitten wird.

## benutzen

das skript zeigt nur einmal die abfahrten an, wenn es im loop laufen soll kann man einfach einen loop in der shell machen:
```sh
while true; ./abfahrten.py; sleep 20; end
```

## etc 

es gibt bei verspätungen oder bei ersatzlinien (die haben sehr lange liniennummern) noch paar anomalien in der darstellung, aber da das so selten vorkommt hatte ich mich jetzt nicht im detail mit allem beschäftigt.

ich mache das grad nur für bus und tram aber geht auch für sbahn und fern/regionalverkehr, dazu die transport.rest [doku](https://v6.db.transport.rest/api.html). ggf. müssen die filterregexes auch noch angepasst werden, da ich z.b. strings wie "SEV" rausfiltere.


---

danke an [transport.rest](https://transport.rest/), die die deutsche bahn api tatsächllich benutzbar machen <3


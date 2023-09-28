#!/usr/bin/env python3
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import re
import math
from time import sleep
import tomllib

with open("./abfahrten.toml", mode="rb") as f:
    cfg = tomllib.load(f)

station = cfg["general"]["station_id"]
maxres = cfg["general"]["max_results"]
url = "https://v6.db.transport.rest/stops/"+str(station)+"/departures"
deps = list()

dir_override = cfg["direction_overrides"]

def print_departures(out):
# 1 minute pause between intervals, prevent dups
    for interval in [0, 11, 22, 33]:
        if len(deps) >= maxres:
            break
        params = {
            "bus" : "true",
            "tram" : "true",
            "results" : 5,
            "when" : "in "+str(interval)+" minutes"
        }

        try:
            res = requests.get(url=url, params=params)
        except OSError:
            print("api connection failed")
            continue

        data = res.json()
        for dep in data["departures"]:
            deps.append(dep)
            if len(deps) >= maxres:
                break

    if len(deps) == 0:
        print("no departures within 30 min")

    for idx, dep in enumerate(deps):
        leaving = datetime.fromisoformat(dep["plannedWhen"])
        now = datetime.now(ZoneInfo("Europe/Berlin"))
        leaving_raw = (leaving-now).total_seconds()+30

        leaving_in = round(leaving_raw / 60)
        leaving_in_str = str(0) if leaving_in <= 0 else str(leaving_in)

        if type(dep["delay"]) == int and dep["delay"] > 0:
            leaving_in_str += "+"+str(round(dep["delay"]/60))

        line_nr = re.sub("^(Bus|STR) *", "", dep["line"]["name"])
        line_filter_sev = re.sub("^SEV", "", line_nr)
        
        out += line_filter_sev.ljust(3)

        try:
            direction = dir_override[dep["direction"]]
        except KeyError as e:
            if ">" in dep["direction"]:
                # wird nach endhaltestelle zu ner anderen linie
                # aber das ist uns egal wo der dann hinfährt
                direction = dir_override[dep["direction"].split(">")[0].strip()]
            else:
                direction = dep["direction"][:18]
                #print("\nnot in direction map:", e)

        out += direction.ljust(20)
        out += leaving_in_str.ljust(5)

        info = ""
        if len(dep["remarks"]) != 0:
            info = "*"

        if idx+1 == maxres:
            out += f"min{info}"
        else:
            out += f"min{info}\n"

    print(out, end="")
    # always print $maxres lines, pad with \n if necessary
    print("\n" * (maxres - len(deps)), end="")

time = datetime.now().strftime("%H:%M:%S")
out = f"\nAbfahrten {cfg['general']['station_name']} {time}\n"
print_departures(out)


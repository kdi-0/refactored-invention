import json
import lcu
connector = lcu.LCU_Client()
current_summoner = connector("GET", "/lol-summoner/v1/current-summoner").json()
res = connector(
    "GET", f"/lol-match-history/v1/products/lol/{current_summoner['puuid']}/matches?begIndex=0&endIndex=10").json()
gamelist = res["games"]["games"]

print(type(gamelist))
print([game["participants"][0]["stats"]["win"] for game in gamelist])
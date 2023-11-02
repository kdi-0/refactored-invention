from flask import Flask
import lcu
import json

from flask_cors import CORS
from flask_cors import cross_origin
import logging
connector = lcu.LCU_Client()
app = Flask(__name__)
CORS(app)

# id to queue name
queueIdToName = {"450": "ARAM", "420": "Ranked Solo/Duo",
                 "1300": "Nexus Blitz", "400": "Normal (Draft Pick)"}

logging.getLogger('flask_cors').level = logging.DEBUG


class Match:
    def __init__(self, result: str, champion: str, kills: str, deaths: str,
                 assists: str, queueType: str, gameDuration: str):
        self.result = result
        self.champion = champion
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.queueName = queueType
        self.gameDuration = gameDuration


class MatchHistory:
    matches: list[Match]


class SummonerInfo:
    def __init__(self, name: str, puuid: str, accountId: str, wins: str, losses: str, rank_tier: str, rank_division: str):
        self.display_name = name
        self.puuid = puuid
        self.accountId = accountId
        self.wins = wins
        self.losses = losses
        self.rank_tier = rank_tier
        self.rank_division = rank_division

    def __str__(self):
        return f"SummonerInfo(name={self.name}, puuid={self.puuid}, summonerLevel={self.summonerLevel}, accountId={self.accountId}, id={self.id})"

    def __repr__(self):
        return self.__str__()


def get_summoner_info() -> SummonerInfo:
    res = connector("GET", "/lol-summoner/v1/current-summoner")
    data = res.json()
    puuid = data["puuid"]
    ranked_stats = connector(
        "GET", f"/lol-ranked/v1/ranked-stats/{puuid}").json()["queueMap"]["RANKED_SOLO_5x5"]
    return SummonerInfo(
        name=data["displayName"],
        puuid=data["puuid"],
        accountId=data["accountId"],
        wins=ranked_stats["wins"],
        losses=ranked_stats["losses"],
        rank_tier=ranked_stats["tier"],
        rank_division=ranked_stats["division"]
    )

def getMatchInfo(match: dict):
    gameId = match["gameId"]
    gameDuration = match["gameDuration"]
    queueId = match["queueId"]
    queueName = queueIdToName[str(queueId)] if str(queueId) in queueIdToName else "Unknown"
    participant = match["participants"][0]
    champion = participant["championId"]
    kills = participant["stats"]["kills"]
    deaths = participant["stats"]["deaths"]
    assists = participant["stats"]["assists"]
    win = "Win" if participant["stats"]["win"] else "Loss"
    #return everything above as dict
    return {
        "gameId": gameId,
        "gameDuration": gameDuration,
        "queueName": queueName,
        "champion": champion,
        "kills": kills,
        "deaths": deaths,
        "assists": assists,
        "win": win
    }


@app.get('/matchHistory')
@cross_origin()
def matchHistory():
    current_summoner = get_summoner_info()
    res = connector(
        "GET", f"/lol-match-history/v1/products/lol/{current_summoner.puuid}/matches?begIndex=0&endIndex=10").json()
    gamelist = res["games"]["games"]
    match_details = [getMatchInfo(game) for game in gamelist]
    return match_details
    


@app.get('/summonerInfo')
@cross_origin()
def summonerInfo():
    current_summoner = get_summoner_info()
    return {
        "name": current_summoner.display_name,
        "puuid": current_summoner.puuid,
        "accountId": current_summoner.accountId,
        "wins": current_summoner.wins,
        "losses": current_summoner.losses,
        "rank_tier": current_summoner.rank_tier,
        "rank_division": current_summoner.rank_division
    }
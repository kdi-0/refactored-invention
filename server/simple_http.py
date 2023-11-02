from lcu import LCU_Client
import json
if __name__ == "__main__":
    lcu = LCU_Client()
    res = lcu("GET", "/lol-summoner/v1/current-summoner")
    # write to file in formatted form
    with open("lol-summoner_v1_current-summoner.json", "w") as f:
        f.write(json.dumps(res.text, indent=4))
    data = res.json()
    # res = lcu(
    #     "GET", f"/lol-match-history/v1/products/lol/{data['puuid']}/matches?begIndex=0&endIndex=10")
    # # write to file in formatted form
    # with open("lol-match-history_v1_products_lol_puuid_matches.json", "w") as f:
    #     f.write(json.dumps(res.json(), indent=4))

    # testing /lol-gameflow/v1/session
    res = lcu("GET", "/lol-gameflow/v1/session")
    # write to file in formatted form
    with open("lol-gameflow_v1_session.json", "a") as f:
        f.write(json.dumps(res.json(), indent=4))
    
    res = lcu("GET", "/lol-game-queues/v1/queues")
    with open("lol-game-queues_v1_queues.json", "a") as f:
        f.write(json.dumps(res.json(), indent=4))
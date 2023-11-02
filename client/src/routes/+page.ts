import type { PageLoad } from "./$types";

interface Champion {
    version: string;
    id: string;
    key: string;
    name: string;
    title: string;
    blurb: string;
    info: {
        attack: number;
        defense: number;
        magic: number;
        difficulty: number;
    };
    image: {
        full: string;
        sprite: string;
        group: string;
        x: number;
        y: number;
        w: number;
        h: number;
    };
    tags: string[];
    partype: string;
    stats: {
        hp: number;
        hpperlevel: number;
        mp: number;
        mpperlevel: number;
        movespeed: number;
        armor: number;
        armorperlevel: number;
        spellblock: number;
        spellblockperlevel: number;
        attackrange: number;
        hpregen: number;
        hpregenperlevel: number;
        mpregen: number;
        mpregenperlevel: number;
        crit: number;
        critperlevel: number;
        attackdamage: number;
        attackdamageperlevel: number;
        attackspeedperlevel: number;
        attackspeed: number;
    };
}

interface ChampionData {
    [key: string]: Champion;
}
const createKeyToNameMapping = (data: ChampionData): { [key: string]: string } => {
    const mapping: { [key: string]: string } = {};
    for (const champion in data) {
        if (data.hasOwnProperty(champion)) {
            const { key, name } = data[champion];
            mapping[key] = name;
        }
    }
    return mapping;
};

export const load: PageLoad = async ({ fetch }) => {
    const summoner_res = await fetch("http://127.0.0.1:5000/summonerInfo", {
        method: "GET",
        mode: "cors",
    });
    const summoner_info = await summoner_res.json();
    const match_history_res = await fetch("http://127.0.0.1:5000/matchHistory", {
        method: "GET",
        mode: "cors",
    });
    const match_history = await match_history_res.json();
    const champion_mapping_res = await fetch("https://ddragon.leagueoflegends.com/cdn/13.21.1/data/en_US/champion.json", {
        "method": "GET"
    });

    const champion_data = await champion_mapping_res.json();
    const champ_mapped = createKeyToNameMapping(champion_data.data);
    return { summoner_info, match_history, champ_mapped };
};
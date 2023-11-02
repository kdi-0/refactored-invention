<script lang="ts">
    import RankWidget from "./RankWidget.svelte";
    import Match from "./Match.svelte";
    import type {PageData} from './$types';
    export let data: PageData;
</script>

<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
<style>
    .textapply {
        font-family: 'Roboto', sans-serif;
    }
    .center-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    }
</style>

<div class="textapply">
    <div class="center-wrapper">
    {#await data.summoner_info}
        Loading summoner..
    {:then summoner}
        <RankWidget summonerName={summoner.name} rank_division={summoner.rank_division} rank_tier={summoner.rank_tier} winRate={(summoner.wins/(summoner.wins+summoner.losses))*100} wins={summoner.wins} losses={summoner.losses} />
    {:catch error}
        <p style="color: red">{error.message}</p>
    {/await}
    </div>
    {#await data.match_history then history}
        {#each history as m}
            <Match mode={m.queueName} outcome={m.win} assists={m.assists} kills={m.kills} deaths={m.deaths} matchId={m.gameId} champion={data.champ_mapped[m.champion]} />
        {/each}
    {/await}
</div>
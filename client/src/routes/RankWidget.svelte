<!-- src/routes/RankWidget.svelte -->
<script lang="ts">
  export let rank_tier: string;
  export let rank_division: string;
  export let winRate: number;
  export let wins: number;
  export let losses: number;
  export let summonerName: string;
</script>

<div class="rank-container">
  <img
    src="/league/Ranked_Emblems_Latest/Rank={rank_tier}.png"
    alt={rank_tier}
    class="emblem"
  />
  <div class="details">
    <h2>{summonerName}</h2>
    <h3>{rank_tier + " " + rank_division}</h3>
    <p>Win Rate {winRate.toFixed(2)}%</p>
    <p>{wins}W {losses}L</p>
  </div>
</div>

<style>
  .rank-container {
    display: flex;
    flex-direction: row; /* Change here */
    align-items: center;
    background-color: #ffffff93;
    padding: 1rem;
    border-radius: 5px;
    gap: 20px;
  }

  .emblem {
    width: 110px;
    height: 110px;
  }

  .details {
    margin-left: 1rem; /* Added to give some spacing between the emblem and details */
    text-align: left; /* Change to left */
  }
</style>

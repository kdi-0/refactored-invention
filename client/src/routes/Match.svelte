<script lang="ts">
    export let mode: string;
    export let outcome: string; // either Win or Loss
    export let assists: string;
    export let kills: string;
    export let deaths: string;
    export let matchId: number;
    export let champion: string;
</script>

<div class={"match-container " + outcome}>
    <div class="match-details">
        <img class="img" src={"/champion/" + champion + ".png"} alt={champion} />
        <p class={outcome === "Win" ? "victory" : "defeat"}>{outcome}</p>
        <p>{champion}</p>
        <p>{mode + "\t"}</p>
        <p>{kills}/{deaths}/{assists}</p>
        <p>Match ID: {matchId}</p>
    </div>
</div>

<style>
    .img {
        width: 70px;
        height: 70px;
    }
    .match-details {
        text-align: center;
        display: flex;
        justify-content: space-around; /* Distribute children evenly */
        align-items: center;
        width: 100%; /* Take up full width of parent */
    }

    .match-container {
        display: flex;
        align-items: center;
        padding: 1rem;
        border-bottom: 1px solid #b4b4b4;
        width: 80%; /* Reduce width to 90% */
        margin: 0.5rem auto; /* Center container horizontally and add spacing between rows */
        box-sizing: border-box; /* Ensure padding doesn't add to the width */
    }

    .match-container.Win {
        background-color: #c4ffc4; /* Light green for victory rows */
    }

    .match-container.Loss {
        background-color: #ffc3c3; /* Light red for defeat rows */
    }

    .defeat {
        color: red;
    }

    .victory {
        color: green;
    }
</style>

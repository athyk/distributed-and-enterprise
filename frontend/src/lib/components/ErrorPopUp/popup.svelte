<script lang="ts">
    export let errorMessage = '';
</script>

{#if errorMessage}
    <div class="bg-red-500 text-white p-4 mb-4 rounded shadow-lg w-full">
        <p>{errorMessage}</p>
        <button class="mt-2 bg-white text-red-500 px-2 py-1 rounded" on:click={() => errorMessage = ''}>Close</button>
    </div>
{/if}
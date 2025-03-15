<script lang="ts">
    export let tags = [] as string[];
</script>

<div class="flex space-x-2 overflow-x-auto whitespace-nowrap scrollbar-thin scrollbar-thumb-gray-500 scrollbar-track-gray-200 py-2">
    {#each tags as tag}
        <span class="bg-gray-100 text-black mt-3 p-2 rounded-xl">#{tag}</span>
    {/each}
</div>
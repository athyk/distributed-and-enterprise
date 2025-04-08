<script lang="ts">
	export let tags = [] as string[];
</script>

<div
	class="scrollbar-thin scrollbar-thumb-gray-500 scrollbar-track-gray-200 flex space-x-2 overflow-x-auto py-2 whitespace-nowrap"
>
	{#each tags as tag}
		<span class="mt-3 rounded-xl bg-gray-200 p-2 text-black shadow-md">#{tag}</span>
	{/each}
</div>

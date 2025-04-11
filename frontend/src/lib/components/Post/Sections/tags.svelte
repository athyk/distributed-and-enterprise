<script lang="ts">
	export let tags = [] as string[];
</script>

<div class="flex flex-wrap gap-2 py-2">
	{#each tags as tag}
		<span class="mt-3 rounded-xl bg-gray-200 p-2 text-black shadow-md">#{tag}</span>
	{/each}
</div>

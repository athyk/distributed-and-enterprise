<script lang="ts">
	import { onMount } from 'svelte';
	import { get } from '$lib/api/get';
	import type { PaginationDataResponse, PaginationData } from '$lib/api/apiType';

	// Initialize an empty array for community tags.
	let communityTags: PaginationData[] = [];

	// Fetch community tags from the API endpoint.
	async function fetchCommunityTags() {
		console.log('Fetching community tags...');
		try {
			const response: PaginationDataResponse = await get('tags/list/');
			console.log('Community tags fetched:', response);

			communityTags = response.tags;
		} catch (error) {
			console.error('Error fetching community tags:', error);
		}
	}

	// Fetch tags when the component mounts.
	onMount(fetchCommunityTags);
</script>

<main class="flex h-screen">
	<!-- Sidebar -->
	<aside
		class="fixed top-0 left-0 h-full w-64 overflow-y-auto bg-gray-900 px-4 py-6 text-white shadow-lg"
	>
		<h2 class="mb-4 text-xl font-bold">Community Tags</h2>

		{#if communityTags && communityTags.length > 0}
			<ul class="space-y-3">
				{#each communityTags as tag (tag.name)}
					<li
						class="flex items-center space-x-3 rounded-md bg-gray-800 p-3 shadow-md transition hover:bg-gray-700"
					>
						<input type="checkbox" id={tag.name} class="form-checkbox h-5 w-5 text-blue-500" />
						<label for={tag.name} class="cursor-pointer text-lg font-semibold">{tag.name}</label>
						<span class="text-sm text-gray-400">({tag.count})</span>
					</li>
				{/each}
			</ul>
		{:else}
			<p class="text-gray-400">No community tags found.</p>
		{/if}
	</aside>
</main>

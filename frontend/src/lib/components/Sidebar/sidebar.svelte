<script lang="ts">
	import { onMount } from 'svelte';
	import { get } from '$lib/api/get';
	import type { PaginationDataResponse ,PaginationData} from "$lib/api/apiType";




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
	<aside class="w-64 bg-gray-900 text-white h-full fixed left-0 top-0 py-6 px-4 shadow-lg overflow-y-auto">
		<h2 class="text-xl font-bold mb-4">Community Tags</h2>

		{#if communityTags && communityTags.length > 0}
			<ul class="space-y-3">
				{#each communityTags as tag (tag.name)}
					<li class="flex items-center space-x-3 p-3 bg-gray-800 rounded-md shadow-md hover:bg-gray-700 transition">
						<input type="checkbox" id={tag.name} class="form-checkbox h-5 w-5 text-blue-500" />
						<label for={tag.name} class="text-lg font-semibold cursor-pointer">{tag.name}</label>
						<span class="text-gray-400 text-sm">({tag.count})</span>
					</li>
				{/each}
			</ul>
		{:else}
			<p class="text-gray-400">No community tags found.</p>
		{/if}
	</aside>


</main>

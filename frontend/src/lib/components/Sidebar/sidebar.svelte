<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { get } from '$lib/api/get';
	import type { PaginationDataResponse, PaginationData } from '$lib/api/apiType';

	// Event dispatcher to communicate with parent components
	const dispatch = createEventDispatcher();

	// Component state
	let communityTags = [];
	let selectedTags = [];
	let isLoading = true;
	let error = null;

	// Fetch community tags from the API endpoint
	async function fetchCommunityTags() {
		isLoading = true;
		error = null;
		
		try {
			const response = await get('tags/list/');
			console.log('Tags response:', response); // Debug log to see actual response structure
			
			// Handle different possible response structures
			if (response && response.tags) {
				communityTags = response.tags;
			} else if (Array.isArray(response)) {
				communityTags = response;
			} else {
				communityTags = [];
			}
		} catch (err) {
			console.error('Error fetching tags:', err);
			error = "Failed to load tags. Please try again later.";
			communityTags = [];
		} finally {
			isLoading = false;
		}
	}

	// Handle tag selection - uses tag name as the identifier for simplicity
	function toggleTag(tag) {
		// Get the tag name, handling both string tags and object tags
		const tagName = typeof tag === 'string' ? tag : tag.name;
		
		// Toggle selection state
		if (selectedTags.includes(tagName)) {
			selectedTags = selectedTags.filter(t => t !== tagName);
		} else {
			selectedTags = [...selectedTags, tagName];
		}
		
		// Notify parent component
		dispatch('tagselection', { selectedTags });
	}

	// Clear all selected tags
	function clearAllTags() {
		selectedTags = [];
		dispatch('tagselection', { selectedTags });
	}

	// Fetch tags when the component mounts
	onMount(fetchCommunityTags);
</script>

<aside class="fixed top-0 left-0 h-full w-64 overflow-y-auto bg-gray-900 px-4 py-6 text-white shadow-lg">
	<h2 class="mb-4 text-xl font-bold">Filter by Tags</h2>
	
	<!-- Loading state -->
	{#if isLoading}
		<div class="flex justify-center py-4">
			<div class="h-6 w-6 animate-spin rounded-full border-t-2 border-white"></div>
		</div>
	<!-- Error state -->
	{:else if error}
		<p class="rounded-md bg-red-800 p-3 text-sm">{error}</p>
	<!-- Empty state -->
	{:else if !communityTags || communityTags.length === 0}
		<p class="text-gray-400">No tags available.</p>
	<!-- Tag list -->
	{:else}
		<ul class="space-y-2">
			{#each communityTags as tag}
				{#if tag}
					{@const tagName = typeof tag === 'string' ? tag : (tag.name || 'Unknown')}
					{@const tagCount = typeof tag === 'object' && tag.count !== undefined ? tag.count : 0}
					
					<li>
						<button 
							class="flex w-full items-center rounded-md {selectedTags.includes(tagName) ? 'bg-blue-700' : 'bg-gray-800'} p-2.5 text-left transition hover:bg-gray-700"
							on:click={() => toggleTag(tag)}
						>
							<span class="mr-2 inline-block h-4 w-4 rounded-sm border border-gray-400 {selectedTags.includes(tagName) ? 'bg-blue-500' : ''}"></span>
							<span class="text-sm font-medium">{tagName}</span>
							{#if tagCount > 0}
								<span class="ml-auto text-xs text-gray-400">({tagCount})</span>
							{/if}
						</button>
					</li>
				{/if}
			{/each}
		</ul>
		
		<!-- Clear filters button (only shows when tags are selected) -->
		{#if selectedTags.length > 0}
			<div class="mt-6 border-t border-gray-700 pt-4">
				<button 
					class="w-full rounded-md bg-red-600 py-2 text-sm font-medium hover:bg-red-700"
					on:click={clearAllTags}
				>
					Clear All Filters ({selectedTags.length})
				</button>
			</div>
		{/if}
	{/if}
</aside>

<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { get } from '$lib/api/get';

	import SearchBox from '$components/SearchBox/searchBox.svelte';
    
	// Define data structures
	let tags: any[] = [];
	let selectedTags: any[] = [];
	let degree: any[] = [];
	let selectedDegree: any = null;

	// Toggle states
	let isCommunityTagsOpen = true;
	let isDegreeOpen = true;

	// Loading states
	let isLoadingTags = true;
	let tagsError: string | null = null;
	
	const dispatch = createEventDispatcher();

	// Fetch initial data
	onMount(async () => {
		try {
			const tagsResponse = await get('tags/list/');
			tags = tagsResponse.data || [];
			isLoadingTags = false;
		} catch (error) {
			tagsError = "Failed to load tags";
			isLoadingTags = false;
		}
	});

	// Watch for changes in the selected tags
	$: {
		if (tags.length) {
			selectedTags = tags.filter(tag => tag.selected);
		}
	}

	// Watch for changes in the selected degree
	$: {
		if (degree.length) {
			selectedDegree = degree.find(d => d.selected);
		}
	}

	// Clear functions
	function clearAllTags() {
		tags = tags.map(tag => ({...tag, selected: false}));
		selectedTags = [];
	}

	function clearDegree() {
		degree = degree.map(d => ({...d, selected: false}));
		selectedDegree = null;
	}

	// Toggle sections
	function toggleCommunityTags() {
		isCommunityTagsOpen = !isCommunityTagsOpen;
	}

	function toggleDegree() {
		isDegreeOpen = !isDegreeOpen;
	}
</script>

<aside class="fixed top-16 left-0 bottom-0 w-72 overflow-y-auto bg-gray-900 px-4 py-6 text-white shadow-lg">
	<div class="mb-6">
		<h2 class="mb-3 text-xl font-bold">Filters</h2>
		
		<!-- Community Tags with Search -->
		<div class="mb-6">
			<div class="flex items-center justify-between">
				<button 
					class="flex items-center text-lg font-semibold"
					on:click={toggleCommunityTags}
				>
					<span>Community Tags</span>
				</button>

				{#if selectedTags.length > 0}
					<button 
						on:click={clearAllTags}
						class="text-xs text-red-400 hover:text-red-300"
					>
						Clear ({selectedTags.length})
					</button>
				{/if}
			</div>
			
			{#if isCommunityTagsOpen}
				<div class="mt-2">
					<SearchBox
						classStyle="w-full bg-gray-800 border border-gray-700 rounded-lg p-2 focus:outline-none focus:border-blue-500 text-white"
						marginTop=""
						placeholder="Search for Tags..."
						url="tags/list/"
						multi_select={true}
						max_select={5}
						bind:selected={tags}
					/>
					
					{#if isLoadingTags}
						<p class="mt-2 text-gray-400">Loading tags...</p>
					{:else if tagsError}
						<p class="mt-2 text-red-400">{tagsError}</p>
					{:else if selectedTags.length > 0}
						<div class="mt-3 flex flex-wrap gap-2">
							{#each selectedTags as tag}
								<span class="inline-flex items-center rounded-full bg-blue-700 px-2.5 py-0.5 text-xs font-medium">
									{tag.name}
								</span>
							{/each}
						</div>
					{/if}
				</div>
			{/if}
		</div>

		<!-- Degree Filter -->
		<div class="mb-6">
			<div class="flex items-center justify-between">
				<button 
					class="flex items-center text-lg font-semibold"
					on:click={toggleDegree}
				>
					<span>Degree</span>
				</button>

				{#if selectedDegree}
					<button 
						on:click={clearDegree}
						class="text-xs text-red-400 hover:text-red-300"
					>
						Clear
					</button>
				{/if}
			</div>
			
			{#if isDegreeOpen}
				<div class="mt-2">
					<SearchBox
						classStyle="w-full bg-gray-800 border border-gray-700 rounded-lg p-2 focus:outline-none focus:border-blue-500 text-white"
						marginTop=""
						placeholder="Search for Degree..."
						url="degrees/list/"
						multi_select={false}

					/>
					
					{#if selectedDegree}
						<div class="mt-3">
							<span class="inline-flex items-center rounded-full bg-green-700 px-2.5 py-0.5 text-xs font-medium">
								{selectedDegree.name}
							</span>
						</div>
					{/if}
				</div>
			{/if}
		</div>
	</div>
</aside>

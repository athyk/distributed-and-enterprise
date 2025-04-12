<script lang="ts">
	import { onMount } from 'svelte';
	import CommunityCard from '$lib/components/communityCard/communityCard.svelte'; // Adjust path if needed

	// --- Type Definition for a Community (assuming API returns this structure) ---
	interface Community {
		id: number;
		name: string;
		isPublic: boolean;
		description: string;
		tags: string[];
		degrees: string[];
		totalMembers: number;
		creationDate: string;
	}

	// --- State ---
	let searchQuery: string = '';
	let communities: Community[] = []; // Holds the fetched communities
	let isLoading: boolean = true; // Track loading state
	let error: string | null = null; // Track potential fetch errors
	let initialLoadComplete: boolean = false; // Track if initial load finished

	// --- API Configuration ---
	const API_BASE_URL = 'http://localhost:8000'; // Use http:// if not HTTPS

	// --- Debounce Timer ---
	let debounceTimer: number;

	// --- Fetch Function ---
	async function fetchCommunities(query: string = ''): Promise<void> {
		// 1. Set loading state and clear previous errors
		isLoading = true;
		error = null;
		console.log(`Fetching communities for query: "${query}"`); // Useful for debugging

		try {
			// 2. Construct the URL with the query parameter if provided
			const url = new URL(`${API_BASE_URL}/community/search`);
			const trimmedQuery = query.trim(); // Trim whitespace
			if (trimmedQuery) {
				url.searchParams.append('q', trimmedQuery); // Use 'q' as the parameter name (adjust if different)
			}

			// 3. Make the API call
			const response = await fetch(url.toString());

			// 4. Check if the HTTP response status is OK (e.g., 200-299)
			if (!response.ok) {
				// Throw an error for bad responses (4xx, 5xx)
				throw new Error(`API Error: ${response.status} ${response.statusText}`);
			}

			// 5. Parse the JSON response body
			//    This assumes the API returns a JSON array matching the Community interface on success
			const data: Community[] = await response.json();

			// 6. Update the component's state with the fetched data
			communities = data;

		} catch (err: any) { // Catch network errors or errors thrown above
			// 7. Handle errors
			console.error('Failed to fetch communities:', err);
			// Set an error message for the UI
			error = err instanceof Error ? err.message : 'Failed to load communities. Please try again later.';
			// Clear communities array on error to avoid showing stale data
			communities = [];
		} finally {
			// 8. Always run this block after try/catch
			isLoading = false; // Set loading state to false
			// Mark initial load complete after the *first* fetch attempt (success or failure)
			if (!initialLoadComplete) {
				initialLoadComplete = true;
			}
		}
	}
	// --- Debounced Search Function ---
	function debouncedSearch(): void {
		clearTimeout(debounceTimer);
		// Only fetch if the user has typed something or cleared the input
		debounceTimer = window.setTimeout(() => {
			fetchCommunities(searchQuery);
		}, 500); // Wait 500ms after the user stops typing
	}

	// --- Explicit Search Function (for button click) ---
	function handleSearchClick(): void {
		clearTimeout(debounceTimer); // Clear any pending debounced search
		fetchCommunities(searchQuery);
	}

	// --- Initial Data Load ---
	onMount(() => {
		fetchCommunities(); // Fetch all communities initially (empty query)
	});

</script>

<div
	class="flex min-h-screen flex-col items-center space-y-12 px-4 py-12 text-gray-900 sm:px-8 md:px-12"
>
	<!-- Search Bar -->
	<div
		class="flex w-full max-w-lg items-center gap-2 rounded-full border border-gray-300 p-3 shadow-sm"
	>
		<input
			type="text"
			bind:value={searchQuery}
			placeholder="Search for a community..."
			class="w-full bg-transparent px-4 text-gray-900 outline-none"
			on:input={debouncedSearch}    
			on:keydown={(e) => { if (e.key === 'Enter') handleSearchClick(); }}
		/>		<button
			on:click={handleSearchClick}    
			class="rounded-full bg-blue-500 px-6 py-3 text-white shadow-md transition hover:bg-blue-600 disabled:opacity-50"
            disabled={isLoading}          
		>
			{#if isLoading && !initialLoadComplete} <!-- Show loading only on initial load inside button for space -->
				Loading...
			{:else}
				Search
			{/if}
		</button>
	</div>

	<!-- Status Messages -->
	{#if isLoading && initialLoadComplete}
		<p class="text-gray-600">Searching...</p>
	{/if}
	{#if error}
		<p class="text-red-600">Error: {error}</p>
	{/if}

	<!-- Community Cards Section -->
	{#if !isLoading && !error}
		{#if communities.length > 0}
			<div class="grid w-full grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
				{#each communities as community (community.id)}
					<CommunityCard
						name={community.name}
						isPublic={community.isPublic}
						description={community.description}
						tags={community.tags}
						degrees={community.degrees}
						totalMembers={community.totalMembers}
						creationDate={community.creationDate}
					/>
				{/each}
			</div>
		{:else if initialLoadComplete} <!-- Only show 'No results' after the initial load is done -->
			<p class="text-gray-600">No communities found matching your search.</p>
		{/if}
	{/if}

    <!-- Optional: Show initial loading state centered -->
	{#if isLoading && !initialLoadComplete && !error}
		<p class="mt-20 text-gray-600">Loading communities...</p>
	{/if}

</div>
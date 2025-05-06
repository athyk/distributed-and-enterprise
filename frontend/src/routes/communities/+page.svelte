<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import CommunityCard from '$lib/components/communityCard/communityCard.svelte';
	import Sidebar from '$lib/components/Sidebar/sidebar.svelte';

	// --- Type Definitions ---
	interface Tag {
		id: number;
		name: string;
	}

	interface Community {
		id: number;
		name: string;
		isPublic: boolean;
		description: string;
		tags: Tag[];
		degrees: string[];
		totalMembers: number;
		creationDate: string;
	}

	// --- Component State ---
	let searchQuery: string = '';
	let filteredCommunities: Community[] = [];
	let isLoading: boolean = true;
	let error: string | null = null;
	let selectedTags: Tag[] = [];

	// --- API Configuration ---
	const API_BASE_URL = 'http://localhost:8000'; // Ensure this is correct for your setup

	// --- Debounce Timer Reference ---
	let debounceTimer: number;

	// --- Redirect to Create Community Page ---
	function redirectToCreateCommunity(): void {
		// console.log('[redirectToCreateCommunity] Redirecting user to create community page');
		goto('communities/create'); // Adjust this path as needed to match your actual route
	}

	// --- Fetch Function (Reduced Logging) ---
	async function fetchCommunities(query: string = '', tags: Tag[] = []): Promise<void> {
		isLoading = true;
		error = null;
		// Log: Function entry point with parameters (Kept for context)
		console.log(`[fetchCommunities] Called with query: "${query}", tags:`, JSON.stringify(tags.map(t => t.id)));

		try {
			const url = new URL(`${API_BASE_URL}/community/search`);
			const trimmedQuery = query.trim();

			if (trimmedQuery) {
				url.searchParams.append('name', trimmedQuery);
			}

			if (tags && tags.length > 0) {
				// Filter out any undefined or invalid tags before mapping
				const validTags = tags.filter(tag => tag && typeof tag === 'object' && typeof tag.id === 'number'); // Stricter check for number ID

				if (validTags.length > 0) {
					const tagIds = validTags.map(tag => tag.id.toString()); // Convert number ID to string

					if (tagIds.length > 0) {
						url.searchParams.append('tags', tagIds.join(','));
						// Log: Tag IDs being appended to URL (Kept as requested)
						console.log('[fetchCommunities] Appended Tag IDs to URL:', tagIds.join(','));
					}
				} else {
					// Warn if tags were provided but none were valid (Kept)
                    console.warn('[fetchCommunities] No valid tags found in selected tags array passed to fetch.', tags);
				}
			}

			// Log: The final URL being requested (Kept for debugging)
			console.log('[fetchCommunities] Requesting URL:', url.toString());
			const response = await fetch(url.toString());

			if (!response.ok) {
				throw new Error(`API Error: ${response.status} ${response.statusText}`);
			}

			const data = await response.json();
			// console.log('[fetchCommunities] Raw API Response Data:', data); // Removed

			let communitiesData: Community[];

			// --- Adjust based on your actual API response structure ---
			if (Array.isArray(data)) {
				communitiesData = data;
			} else if (data.communities && Array.isArray(data.communities)) {
				communitiesData = data.communities;
			} else if (data.results && Array.isArray(data.results)) {
				communitiesData = data.results;
			} else if (data.data && Array.isArray(data.data)) {
                communitiesData = data.data;
            } else if (typeof data === 'object' && data !== null && !Array.isArray(data)) {
                // Handle case where API returns a single object instead of array for one result?
                communitiesData = [data];
            }
			else {
				throw new Error('Unexpected API response format. Expected an array or object containing an array of communities.');
			}
			// --- End structure adjustment ---

			// console.log('[fetchCommunities] Identified Communities Data:', communitiesData); // Removed

			// Process and map communities
			filteredCommunities = communitiesData.map(community => {
                // Basic validation for tags structure within each community from API
                const processedTags = Array.isArray(community.tags)
                    ? community.tags
                            .map(tag => {
                                // Expecting tags from API to have id (number) and name (string)
                                if (typeof tag === 'object' && tag !== null && typeof tag.id === 'number' && typeof tag.name === 'string') {
                                    return { id: tag.id, name: tag.name };
                                }
                                // Log warning if a tag format is unexpected (Kept)
                                console.warn(`[fetchCommunities] Unexpected API tag format in community ${community.id}:`, tag);
                                return null; // Or handle as needed
                            })
                            .filter((tag): tag is Tag => tag !== null) // Type guard to filter nulls and satisfy TS
                    : []; // Default to empty array if community.tags isn't an array

                // Provide defaults for potentially missing fields
                return {
                    id: typeof community.id === 'number' ? community.id : Date.now() + Math.random(), // Ensure unique ID if missing
                    name: typeof community.name === 'string' ? community.name : 'Unnamed Community',
                    isPublic: typeof community.isPublic === 'boolean' ? community.isPublic : true,
                    description: typeof community.description === 'string' ? community.description : 'No description available',
                    tags: processedTags, // Assign the processed tags
                    degrees: Array.isArray(community.degrees) ? community.degrees.filter(d => typeof d === 'string') : [], // Ensure degrees are strings
                    totalMembers: typeof community.totalMembers === 'number' ? community.totalMembers : 0,
                    creationDate: typeof community.creationDate === 'string' ? community.creationDate : new Date().toISOString()
                };
            });

			// console.log('[fetchCommunities] Processed filteredCommunities:', JSON.stringify(filteredCommunities)); // Removed

		} catch (err: any) {
			// Keep error logging
			console.error('[fetchCommunities] Failed to fetch communities:', err);
			error = err instanceof Error ? err.message : 'Failed to load communities. Please try again later.';
			filteredCommunities = []; // Reset on error
		} finally {
			isLoading = false;
			// console.log('[fetchCommunities] Fetch complete. isLoading:', isLoading); // Removed
		}
	}

	// --- Handle tag selection from sidebar (Reduced Logging) ---
	function handleTagSelection(event: CustomEvent<{ selectedTags: Tag[] }>): void {
		// console.log('[handleTagSelection] Received tag selection event. Detail:', JSON.stringify(event.detail)); // Removed

		if (event.detail && Array.isArray(event.detail.selectedTags)) {
            const receivedTags = event.detail.selectedTags;
            // Ensure received tags match expected structure before assigning
            selectedTags = receivedTags.filter(tag =>
                tag && typeof tag === 'object' && typeof tag.id === 'number' && typeof tag.name === 'string'
            );
            // console.log('[handleTagSelection] Updating selectedTags state to:', JSON.stringify(selectedTags)); // Removed
			// console.log('[handleTagSelection] Triggering fetchCommunities due to tag selection change.'); // Removed
			fetchCommunities(searchQuery, selectedTags);
        } else {
            // Keep warning for unexpected event data
            console.warn("[handleTagSelection] Received invalid tag selection event structure:", event.detail);
            selectedTags = []; // Reset tags if event is invalid
            fetchCommunities(searchQuery, selectedTags); // Refetch with no tags
        }
	}

	// --- Debounced Search Function (Reduced Logging) ---
	function debouncedSearch(): void {
		clearTimeout(debounceTimer);
        // console.log('[debouncedSearch] Input detected, setting timeout.'); // Removed
		debounceTimer = window.setTimeout(() => {
            // console.log(`[debouncedSearch] Timeout finished. Triggering fetchCommunities with query "${searchQuery}" and selected tags:`, JSON.stringify(selectedTags)); // Removed
			fetchCommunities(searchQuery, selectedTags);
		}, 500); // 500ms delay
	}

	// --- Explicit Search Function (Reduced Logging) ---
	function handleSearchClick(): void {
		clearTimeout(debounceTimer); // Clear any pending debounced search
        // console.log(`[handleSearchClick] Search button clicked. Triggering fetchCommunities with query "${searchQuery}" and selected tags:`, JSON.stringify(selectedTags)); // Removed
		fetchCommunities(searchQuery, selectedTags);
	}

    // --- Function to remove a tag and refetch (Reduced Logging) ---
    function removeTag(tagToRemove: Tag): void {
        // console.log('[removeTag] Attempting to remove tag:', JSON.stringify(tagToRemove)); // Removed
        // console.log('[removeTag] Current selectedTags before removal:', JSON.stringify(selectedTags)); // Removed
        selectedTags = selectedTags.filter(t => t.id !== tagToRemove.id);
        // console.log('[removeTag] SelectedTags after removal:', JSON.stringify(selectedTags)); // Removed
        // console.log('[removeTag] Triggering fetchCommunities after removing tag.'); // Removed
        fetchCommunities(searchQuery, selectedTags); // Refetch with updated tags
    }

    // --- Function to clear all tags and refetch (Reduced Logging) ---
    function clearAllTags(): void {
        // console.log('[clearAllTags] Clearing all selected tags.'); // Removed
        // console.log('[clearAllTags] Current selectedTags before clearing:', JSON.stringify(selectedTags)); // Removed
        selectedTags = [];
        // console.log('[clearAllTags] SelectedTags after clearing:', JSON.stringify(selectedTags)); // Removed
        // console.log('[clearAllTags] Triggering fetchCommunities after clearing all tags.'); // Removed
        fetchCommunities(searchQuery, selectedTags); // Refetch with no tags
    }

	// --- Initial Data Load (Reduced Logging) ---
	onMount(() => {
        // console.log('[onMount] Component mounted. Triggering initial fetchCommunities.'); // Removed
		fetchCommunities(); // Fetch all communities initially
	});
</script>

<!-- Component Layout (No changes needed here) -->
<div class="flex min-h-screen bg-gray-50">
	<!-- Sidebar Component -->
	<Sidebar on:tagselection={handleTagSelection} bind:selectedTags /> <!-- Pass selectedTags back for potential sync -->

	<!-- Main Content -->
	<div class="ml-64 flex-1 p-6"> <!-- Adjust ml-64 if sidebar width changes -->
		<div class="mx-auto max-w-6xl">
			<!-- Header with Search Bar and Create Community Button -->
			<div class="mb-8 flex flex-col items-center justify-between gap-4 sm:flex-row">
				<!-- Search Bar Section -->
				<div class="flex w-full max-w-lg items-center gap-2 rounded-full border border-gray-300 bg-white p-2 px-3 shadow-sm focus-within:ring-2 focus-within:ring-blue-500 focus-within:ring-offset-1">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
						<path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
					</svg>
					<input
						type="text"
						bind:value={searchQuery}
						placeholder="Search for a community..."
						class="w-full flex-1 bg-transparent px-2 text-gray-900 outline-none"
						on:input={debouncedSearch}
						on:keydown={(e) => { if (e.key === 'Enter') { e.preventDefault(); handleSearchClick(); } }}
					/>
					<button
						on:click={handleSearchClick}
						class="rounded-full bg-blue-500 px-5 py-1.5 text-sm font-medium text-white shadow-sm transition hover:bg-blue-600 disabled:opacity-50"
						disabled={isLoading}
					>
						{#if isLoading}
							<svg class="h-4 w-4 animate-spin text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
							</svg>
						{:else}
							Search
						{/if}
					</button>
				</div>

				<!-- Create Community Button -->
				<button
					on:click={redirectToCreateCommunity}
					class="flex shrink-0 items-center justify-center gap-2 rounded-lg bg-green-500 px-5 py-2.5 text-sm font-medium text-white shadow-md transition hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
				>
					<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
						<path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
					</svg>
					Create Community
				</button>
			</div>

			<!-- Active Filters Display -->
			{#if selectedTags.length > 0}
				<div class="mb-6 flex flex-wrap items-center gap-2 rounded-lg border border-gray-200 bg-white p-3 shadow-sm">
					<span class="text-sm font-medium text-gray-600">Active filters:</span>
					{#each selectedTags as tag (tag.id)}
						<span class="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-sm font-medium text-blue-800">
							{tag.name}
							<button
								class="ml-1.5 -mr-1 flex-shrink-0 rounded-full p-0.5 inline-flex items-center justify-center text-blue-500 hover:bg-blue-200 hover:text-blue-700 focus:outline-none focus:bg-blue-200"
								aria-label={`Remove ${tag.name} filter`}
								on:click={() => removeTag(tag)}
							>
                                <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                                    <path stroke-linecap="round" stroke-width="1.5" d="M1 1l6 6m0-6L1 7" />
                                </svg>
							</button>
						</span>
					{/each}
					<button
						class="ml-auto text-sm text-blue-600 hover:underline pl-2"
						on:click={clearAllTags}
					>
						Clear all
					</button>
				</div>
			{/if}

			<!-- Display Loading, Error, or Communities -->
			{#if isLoading && filteredCommunities.length === 0} <!-- Show loading spinner only on initial load or when list is empty -->
				<div class="flex justify-center py-12">
					<div class="h-10 w-10 animate-spin rounded-full border-4 border-gray-300 border-t-blue-500"></div>
					<span class="sr-only">Loading communities...</span>
				</div>
			{:else if error}
				<div class="rounded-lg border border-red-200 bg-red-50 p-4 text-center text-red-700 shadow-sm">
					<h3 class="font-medium">Oops! Something went wrong.</h3>
					<p class="text-sm mt-1">{error}</p>
					<button
						on:click={() => fetchCommunities(searchQuery, selectedTags)}
						class="mt-3 inline-flex items-center rounded-md border border-transparent bg-red-100 px-3 py-1.5 text-sm font-medium text-red-700 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:ring-offset-red-50"
					>
						Try Again
					</button>
				</div>
			{:else}
				{#if filteredCommunities.length > 0}
					<div class="grid w-full grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
						{#each filteredCommunities as community (community.id)}
							<CommunityCard
								id={community.id} 
								name={community.name}
								isPublic={community.isPublic}
								description={community.description}
                                tags={community.tags.map(t => t.name)} 
								degrees={community.degrees}
								totalMembers={community.totalMembers}
								creationDate={community.creationDate}
							/>
						{/each}
					</div>
				{:else}
					<!-- Improved "No Results" Message -->
					<div class="flex flex-col items-center justify-center rounded-lg border border-gray-200 bg-white p-8 text-center shadow-sm min-h-[200px]">
						<svg class="h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 10a.01.01 0 01.01-.01M10 10a.01.01 0 00-.01-.01m.01.01H10m0 0v.01M10 10a.01.01 0 01.01.01m0 0a.01.01 0 00-.01.01m0-.01H10m0 0V9.99m0 .01a.01.01 0 00.01-.01m-.01.01H10m0 0V9.99"></path></svg>
						<h3 class="text-lg font-medium text-gray-800">No Communities Found</h3>
						<p class="mt-1 text-sm text-gray-500">
							{#if searchQuery || selectedTags.length > 0}
								Try adjusting your search or filters.
							{:else}
								There are currently no communities listed. Why not create the first one?
							{/if}
						</p>
						{#if !searchQuery && selectedTags.length === 0}
							<button
								on:click={redirectToCreateCommunity}
								class="mt-4 flex items-center justify-center gap-2 rounded-lg bg-green-500 px-4 py-2 text-sm font-medium text-white shadow-md transition hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
							>
								<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
									<path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
								</svg>
								Create Community
							</button>
						{/if}
					</div>
				{/if}
			{/if}
		</div>
	</div>
</div>
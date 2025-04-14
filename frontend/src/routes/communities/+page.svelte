<script lang="ts">
	import { onMount } from 'svelte';
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
	const API_BASE_URL = 'http://localhost:8000';

	// --- Debounce Timer Reference ---
	let debounceTimer: number;

	// --- Fetch Function (Modified with Logging) ---
	async function fetchCommunities(query: string = '', tags: Tag[] = []): Promise<void> {
		isLoading = true;
		error = null;
		// Log: Function entry point with parameters
		console.log(`[fetchCommunities] Called with query: "${query}", tags:`, JSON.stringify(tags));

		try {
			const url = new URL(`${API_BASE_URL}/community/search`);
			const trimmedQuery = query.trim();

			if (trimmedQuery) {
				url.searchParams.append('name', trimmedQuery);
			}

			if (tags.length > 0) {
				const tagIds = tags.map(tag => tag.id);
				// Log: Tag IDs being appended to URL
				console.log('[fetchCommunities] Extracted Tag IDs for API:', tagIds);
				url.searchParams.append('tags', tagIds.join(','));
			}

			// Log: The final URL being requested
			console.log('[fetchCommunities] Requesting URL:', url.toString());
			const response = await fetch(url.toString());

			if (!response.ok) {
				throw new Error(`API Error: ${response.status} ${response.statusText}`);
			}

			const data = await response.json();
			// Log: Raw data received from the API
			console.log('[fetchCommunities] Raw API Response Data:', data);

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
                 communitiesData = [data];
            }
            else {
				throw new Error('Unexpected API response format. Expected an array of communities.');
			}
            // --- End structure adjustment ---

            // Log: Data identified as communities before processing
            console.log('[fetchCommunities] Identified Communities Data:', communitiesData);

			// Process and map communities
			filteredCommunities = communitiesData.map(community => {
				// Basic validation for tags structure within each community from API
				const processedTags = Array.isArray(community.tags)
					? community.tags
							.map(tag => {
								if (typeof tag === 'object' && tag !== null && tag.id !== undefined && tag.name !== undefined) {
									return { id: tag.id, name: tag.name };
								}
								// Log warning if a tag format is unexpected
								console.warn(`[fetchCommunities] Unexpected tag format in community ${community.id}:`, tag);
								return null; // Or handle as needed, maybe return a default tag?
							})
							.filter(tag => tag !== null) // Remove any nulls from unexpected formats
					: []; // Default to empty array if community.tags isn't an array

				return {
					id: community.id || Date.now(),
					name: community.name || 'Unnamed Community',
					isPublic: community.isPublic !== undefined ? community.isPublic : true,
					description: community.description || 'No description available',
					tags: processedTags as Tag[], // Assign the processed tags
					degrees: Array.isArray(community.degrees) ? community.degrees : [],
					totalMembers: community.totalMembers || 0,
					creationDate: community.creationDate || new Date().toISOString()
				};
			});

			// Log: Final processed communities assigned to state
			console.log('[fetchCommunities] Processed filteredCommunities:', JSON.stringify(filteredCommunities));

		} catch (err: any) {
			console.error('[fetchCommunities] Failed to fetch communities:', err);
			error = err instanceof Error ? err.message : 'Failed to load communities. Please try again later.';
			filteredCommunities = [];
		} finally {
			isLoading = false;
			console.log('[fetchCommunities] Fetch complete. isLoading:', isLoading);
		}
	}

	// --- Handle tag selection from sidebar (Modified with Logging) ---
	function handleTagSelection(event: CustomEvent<{ selectedTags: Tag[] }>): void {
		// Log: Raw event detail received
		console.log('[handleTagSelection] Received tag selection event. Detail:', JSON.stringify(event.detail));

		if (event.detail && Array.isArray(event.detail.selectedTags)) {
            const receivedTags = event.detail.selectedTags;
             // Log: Tags assigned to state
            console.log('[handleTagSelection] Updating selectedTags state to:', JSON.stringify(receivedTags));
            selectedTags = receivedTags;
            // Log: Triggering fetch after tag selection
            console.log('[handleTagSelection] Triggering fetchCommunities due to tag selection change.');
			fetchCommunities(searchQuery, selectedTags);
        } else {
            console.warn("[handleTagSelection] Received invalid tag selection event structure:", event.detail);
            // Optionally reset tags or handle appropriately
            console.log('[handleTagSelection] Resetting selectedTags and fetching without filters due to invalid event.');
            selectedTags = [];
            fetchCommunities(searchQuery, selectedTags);
        }
	}

	// --- Debounced Search Function (Modified with Logging) ---
	function debouncedSearch(): void {
		clearTimeout(debounceTimer);
        // Log: Debounce triggered
        console.log('[debouncedSearch] Input detected, setting timeout.');
		debounceTimer = window.setTimeout(() => {
            // Log: Debounce timeout finished, triggering fetch
            console.log(`[debouncedSearch] Timeout finished. Triggering fetchCommunities with query "${searchQuery}" and selected tags:`, JSON.stringify(selectedTags));
			fetchCommunities(searchQuery, selectedTags);
		}, 500);
	}

	// --- Explicit Search Function (Modified with Logging) ---
	function handleSearchClick(): void {
		clearTimeout(debounceTimer);
        // Log: Search button clicked
        console.log(`[handleSearchClick] Search button clicked. Triggering fetchCommunities with query "${searchQuery}" and selected tags:`, JSON.stringify(selectedTags));
		fetchCommunities(searchQuery, selectedTags);
	}

    // --- Function to remove a tag and refetch (Modified with Logging) ---
    function removeTag(tagToRemove: Tag): void {
        // Log: Attempting to remove a tag
        console.log('[removeTag] Attempting to remove tag:', JSON.stringify(tagToRemove));
        console.log('[removeTag] Current selectedTags before removal:', JSON.stringify(selectedTags));
        selectedTags = selectedTags.filter(t => t.id !== tagToRemove.id);
        // Log: State after removal
        console.log('[removeTag] SelectedTags after removal:', JSON.stringify(selectedTags));
        // Log: Triggering fetch after tag removal
        console.log('[removeTag] Triggering fetchCommunities after removing tag.');
        fetchCommunities(searchQuery, selectedTags);
    }

    // --- Function to clear all tags and refetch (Modified with Logging) ---
    function clearAllTags(): void {
        // Log: Clearing all tags
        console.log('[clearAllTags] Clearing all selected tags.');
        console.log('[clearAllTags] Current selectedTags before clearing:', JSON.stringify(selectedTags));
        selectedTags = [];
        // Log: State after clearing
        console.log('[clearAllTags] SelectedTags after clearing:', JSON.stringify(selectedTags));
         // Log: Triggering fetch after clearing tags
        console.log('[clearAllTags] Triggering fetchCommunities after clearing all tags.');
        fetchCommunities(searchQuery, selectedTags);
    }

	// --- Initial Data Load (Modified with Logging) ---
	onMount(() => {
        // Log: Component mounted, triggering initial fetch
        console.log('[onMount] Component mounted. Triggering initial fetchCommunities.');
		fetchCommunities();
	});
</script>

<!-- Component Layout (No changes needed here for logging) -->
<div class="flex min-h-screen bg-gray-50">
	<!-- Sidebar Component -->
	<Sidebar on:tagselection={handleTagSelection} />

	<!-- Main Content -->
	<div class="ml-64 flex-1 p-6">
		<div class="mx-auto max-w-6xl">
			<!-- Search Bar Section -->
			<div class="mb-8 flex w-full max-w-lg items-center gap-2 rounded-full border border-gray-300 bg-white p-3 shadow-sm">
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Search for a community..."
					class="w-full bg-transparent px-4 text-gray-900 outline-none"
					on:input={debouncedSearch}
					on:keydown={(e) => { if (e.key === 'Enter') handleSearchClick(); }}
				/>
				<button
					on:click={handleSearchClick}
					class="rounded-full bg-blue-500 px-6 py-2 text-white shadow-md transition hover:bg-blue-600 disabled:opacity-50"
					disabled={isLoading}
				>
					{isLoading ? 'Loading...' : 'Search'}
				</button>
			</div>

			<!-- Active Filters Display -->
			{#if selectedTags.length > 0}
				<div class="mb-6 flex w-full flex-wrap items-center gap-2">
					<span class="text-sm font-medium text-gray-700">Active filters:</span>
					{#each selectedTags as tag (tag.id)}
						<span class="inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-sm text-blue-800">
							{tag.name}
							<button
								class="ml-1.5 -mr-0.5 flex-shrink-0 p-0.5 rounded-full inline-flex items-center justify-center text-blue-500 hover:bg-blue-200 hover:text-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
								aria-label="Remove {tag.name} filter"
								on:click={() => removeTag(tag)}
							>
                                <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                                    <path stroke-linecap="round" stroke-width="1.5" d="M1 1l6 6m0-6L1 7" />
                                </svg>
							</button>
						</span>
					{/each}
					<button
						class="text-sm text-blue-600 hover:underline ml-2"
						on:click={clearAllTags}
					>
						Clear all
					</button>
				</div>
			{/if}

			<!-- Display Loading, Error, or Communities -->
			{#if isLoading}
				<div class="flex justify-center py-8">
					<div class="h-8 w-8 animate-spin rounded-full border-t-2 border-blue-500"></div>
				</div>
			{:else if error}
				<div class="rounded-lg bg-red-50 p-4 text-red-600">
					<p>Error: {error}</p>
				</div>
			{:else}
				{#if filteredCommunities.length > 0}
					<div class="grid w-full grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
						{#each filteredCommunities as community (community.id)}
							<CommunityCard
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
					<div class="flex h-40 items-center justify-center rounded-lg bg-white p-6 text-center shadow-sm">
						<p class="text-gray-600">
							No communities found matching your search {selectedTags.length > 0 ? 'and filters' : ''}.
						</p>
					</div>
				{/if}
			{/if}
		</div>
	</div>
</div>
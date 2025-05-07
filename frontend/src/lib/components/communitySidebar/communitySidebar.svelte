
<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { get } from '$lib/api/get';
	
	// Define interfaces
	interface Tag {
		id: number;
		name: string;
	}
	
	interface Degree {
		id: number;
		name: string;
		created_at?: number;
		updated_at?: number;
	}
	
	// Component state
	let fetchedTags: Tag[] = [];
	let selectedTags: Tag[] = [];
	let isLoadingTags = true;
	let tagsError: string | null = null;
	
	// Search functionality for tags
	let tagSearchTerm = '';
	
	// Degrees state
	let fetchedDegrees: Degree[] = [];
	let selectedDegrees: Degree[] = [];
	let isLoadingDegrees = true;
	let degreesError: string | null = null;
	let degreeSearchTerm = '';
	
	// Participants range
	let participantsMin = 1;
	let participantsMax = 100;
	let participantsRangeEnabled = false;
	
	// Public status using structured object like in student page
	let queryParams = {
		isPublic: { enabled: false, value: false, label: 'public' }
	};
	
	// State for collapsible sections
	let isCommunityTagsOpen = true;
	let isDegreesOpen = true;
	
	// Event dispatcher for communicating with parent
	const dispatch = createEventDispatcher();
	
	// Get active query parameters to dispatch to parent
	function getActiveQueryParams() {
		const active: Record<string, any> = {};
		
		// Add isPublic if enabled
		const isPublicParam = queryParams.isPublic;
		if (isPublicParam.enabled) {
			active[isPublicParam.label] = isPublicParam.value;
		}
		
		// Add participants range if enabled
		if (participantsRangeEnabled) {
			active['min_participants'] = participantsMin;
			active['max_participants'] = participantsMax;
		}
		
		// Add selected tags and degrees
		if (selectedTags.length > 0) {
			active['tags'] = selectedTags.map(t => t.id);
		}
		
		if (selectedDegrees.length > 0) {
			active['degrees'] = selectedDegrees.map(d => d.id);
		}
		
		return active;
	}
	
	// Dispatch changes to parent component
	function dispatchQueryParamChange() {
		dispatch('queryParamsChange', { activeQueryParams: getActiveQueryParams() });
	}
	
	// Clear all filters and selections
	function clearQueryParams() {
		let changed = false;
		
		// Reset form controls
		for (const k in queryParams) {
			const keyCasted = k as keyof typeof queryParams;
			const p = queryParams[keyCasted];
			if (p.enabled || (keyCasted === 'isPublic' && p.value !== false)) {
				changed = true;
			}
			p.enabled = false;
			if (keyCasted === 'isPublic') {
				p.value = false;
			}
		}
		
		// Reset participants range slider
		if (participantsRangeEnabled) {
			participantsRangeEnabled = false;
			participantsMin = 1;
			participantsMax = 100;
			changed = true;
		}
		
		// Reset tag selections
		if (selectedTags.length > 0) {
			selectedTags = [];
			changed = true;
		}
		
		// Reset degree selections
		if (selectedDegrees.length > 0) {
			selectedDegrees = [];
			changed = true;
		}
		
		if (changed) {
			dispatchQueryParamChange();
			dispatch('tagselection', { selectedTags });
			dispatch('degreeselection', { selectedDegrees });
		}
	}
	
	// Toggle query parameters
	function toggleQueryParam(key: keyof typeof queryParams) {
		queryParams[key].enabled = !queryParams[key].enabled;
		dispatchQueryParamChange();
	}
	
	// Toggle participants range
	function toggleParticipantsRange() {
		participantsRangeEnabled = !participantsRangeEnabled;
		dispatchQueryParamChange();
	}
	
	// Handle range change - fixed to include max
	function handleRangeChange() {
		dispatchQueryParamChange();
	}
	
	// Fetch tags - using get helper like in student page
	async function fetchTags() {
		isLoadingTags = true;
		tagsError = null;
		
		try {
			const responseData = await get<any>('tags/list/');
			const rawTags = responseData?.tags ?? (Array.isArray(responseData) ? responseData : []);
			
			fetchedTags = rawTags
				.map((tagInput: any): Tag | null => {
					// Handle string tag format
					if (typeof tagInput === 'string' && tagInput.trim() !== '') {
						return { id: hashCode(tagInput.trim()), name: tagInput.trim() };
					}
					// Handle object tag format
					if (tagInput && typeof tagInput === 'object') {
						if (typeof tagInput.id === 'number' && typeof tagInput.name === 'string' && tagInput.name.trim() !== '') {
							return { id: tagInput.id, name: tagInput.name.trim() };
						} else if (typeof tagInput.name === 'string' && tagInput.name.trim() !== '') {
							return { id: hashCode(tagInput.name.trim()), name: tagInput.name.trim() };
						}
					}
					console.warn('Skipping malformed tag:', tagInput);
					return null;
				})
				.filter((tag): tag is Tag => tag !== null);
		} catch (err: any) {
			console.error('Error fetching tags:', err);
			tagsError = err instanceof Error ? err.message : 'Failed to load tags. Please try again.';
			fetchedTags = [];
		} finally {
			isLoadingTags = false;
		}
	}
	
	// Generate a simple hash code for string IDs if needed
	function hashCode(str: string): number {
		let hash = 0;
		for (let i = 0; i < str.length; i++) {
			const char = str.charCodeAt(i);
			hash = ((hash << 5) - hash) + char;
			hash = hash & hash; // Convert to 32bit integer
		}
		return Math.abs(hash);
	}
	
	// Fetch degrees - using get helper
	async function fetchDegrees() {
		isLoadingDegrees = true;
		degreesError = null;
		
		try {
			const responseData = await get<any>('degrees/list/');
			
			if (responseData?.success && Array.isArray(responseData.degrees)) {
				fetchedDegrees = responseData.degrees;
			} else if (Array.isArray(responseData)) {
				fetchedDegrees = responseData;
			} else {
				fetchedDegrees = [];
				console.warn('Unexpected degree data format:', responseData);
			}
		} catch (err: any) {
			console.error('Error fetching degrees:', err);
			degreesError = err instanceof Error ? err.message : 'Failed to load degrees. Please try again.';
			fetchedDegrees = [];
		} finally {
			isLoadingDegrees = false;
		}
	}
	
	// Toggle tag selection
	function toggleTag(tag: Tag) {
		const isSelected = selectedTags.some(t => t.id === tag.id);
		
		selectedTags = isSelected
			? selectedTags.filter(t => t.id !== tag.id)
			: [...selectedTags, tag];
			
		dispatch('tagselection', { selectedTags });
		dispatchQueryParamChange();
	}
	
	// Toggle degree selection
	function toggleDegree(degree: Degree) {
		const isSelected = selectedDegrees.some(d => d.id === degree.id);
		
		selectedDegrees = isSelected
			? selectedDegrees.filter(d => d.id !== degree.id)
			: [...selectedDegrees, degree];
			
		dispatch('degreeselection', { selectedDegrees });
		dispatchQueryParamChange();
	}
	
	// Clear all selected tags
	function clearAllTags() {
		if (selectedTags.length > 0) {
			selectedTags = [];
			dispatch('tagselection', { selectedTags });
			dispatchQueryParamChange();
		}
	}
	
	// Clear all selected degrees
	function clearAllDegrees() {
		if (selectedDegrees.length > 0) {
			selectedDegrees = [];
			dispatch('degreeselection', { selectedDegrees });
			dispatchQueryParamChange();
		}
	}
	
	// Initialize component
	onMount(async () => {
		await Promise.all([fetchTags(), fetchDegrees()]);
		// Initial dispatch
		dispatchQueryParamChange();
		dispatch('tagselection', { selectedTags });
		dispatch('degreeselection', { selectedDegrees });
	});
	
	// Reactive declarations for filtering
	$: filteredTags = tagSearchTerm.trim()
		? fetchedTags.filter(tag => 
			tag.name.toLowerCase().includes(tagSearchTerm.toLowerCase())
		)
		: fetchedTags;
		
	$: filteredDegrees = degreeSearchTerm.trim()
		? fetchedDegrees.filter(degree => 
			degree.name.toLowerCase().includes(degreeSearchTerm.toLowerCase())
		)
		: fetchedDegrees;
		
	$: anyQueryParamEnabled = Object.values(queryParams).some(p => p.enabled) || 
							 participantsRangeEnabled || 
							 selectedTags.length > 0 || 
							 selectedDegrees.length > 0;
</script>

<aside class="fixed top-16 left-0 bottom-0 w-72 overflow-y-auto bg-gray-900 px-4 py-6 text-white shadow-lg">
	<div class="mb-6">
		<h2 class="mb-3 text-xl font-bold">Filters</h2>
		
	<!-- Community Tags with Search -->
	<div class="mb-6">
		<button
			on:click={() => isCommunityTagsOpen = !isCommunityTagsOpen}
			class="flex w-full items-center justify-between mb-3 text-xl font-bold hover:text-blue-400 transition-colors"
			aria-expanded={isCommunityTagsOpen}
			aria-controls="community-tags-content"
		>
			Community Tags
			<span class="transform transition-transform duration-200 {isCommunityTagsOpen ? 'rotate-180' : ''}">▼</span>
		</button>
		
		{#if isCommunityTagsOpen}
			<div id="community-tags-content">
				<!-- Search box for tags -->
				<div class="mb-2">
					<input
						type="text"
						placeholder="Search tags..."
						bind:value={tagSearchTerm}
						class="w-full rounded bg-gray-800 p-1.5 text-sm border border-gray-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
					/>
				</div>
				
				{#if isLoadingTags}
					<div class="flex justify-center py-4"><div class="h-6 w-6 animate-spin rounded-full border-t-2 border-b-2 border-blue-500"></div></div>
				{:else if tagsError}
					<p class="rounded-md bg-red-800 p-3 text-sm">{tagsError}</p>
				{:else if !fetchedTags || !fetchedTags.length}
					<p class="text-sm text-gray-400 p-2">No community tags available.</p>
				{:else}
					<ul class="space-y-1 max-h-60 overflow-y-auto pr-1">
						{#each filteredTags as tag (tag.id)}
							{@const isSelected = selectedTags.some(t => t.id === tag.id)}
							<li>
								<button
									on:click={() => toggleTag(tag)}
									class="flex w-full items-center justify-between rounded p-2 text-left text-sm transition-colors {isSelected ? 'bg-blue-700 hover:bg-blue-600' : 'bg-gray-800 hover:bg-gray-700'}"
								>
									<span>{tag.name}</span>
									{#if isSelected}<span class="text-blue-300">✓</span>{/if}
								</button>
							</li>
						{/each}
					</ul>
					
					{#if selectedTags.length > 0}
						<button on:click={clearAllTags} class="mt-3 w-full rounded bg-red-600 py-2 text-sm font-medium hover:bg-red-700 transition-colors">
							Clear Tags ({selectedTags.length})
						</button>
					{/if}
				{/if}
			</div>
		{/if}
	</div>


	</div>
</aside>

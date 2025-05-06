<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	// Removed: import { get } from '$lib/api/get'; // No longer fetching internally if props are provided

	const dispatch = createEventDispatcher();

	// --- Props ---
	// These will be populated by the parent component
	export let degrees: { id: number; name: string }[] = [];
	export let tags: { id: number; name: string }[] = []; // Renamed from 'communityTags' for clarity, maps to parent's 'tags'
	export let isLoading: boolean = false; // Indicates if the parent (student list) is loading

	// --- Component State ---

	// Age range (remains internal to sidebar)
	let ageMin = 18;
	let ageMax = 65;
	let ageRangeEnabled = false;
	
	// Participants range - This seems specific to a different context (e.g. projects, not students).
	// I'll keep it for now, but consider if it's needed for student filtering.
	// If it's for 'year of study' or similar, it should be relabeled.
	// For now, assuming it's a valid filter, though not used by the parent's student filter logic.
	let participantsMin = 1; // Example, if this were for project size etc.
	let participantsMax = 100;
	let participantsRangeEnabled = false;

	let queryParams = {
		gender: { enabled: false, value: '', label: 'gender' },
		isPublic: { enabled: false, value: false, label: 'public' }
	};

	const genderOptions = [
		{ value: 'MALE', label: 'Male' },
		{ value: 'FEMALE', label: 'Female' },
		{ value: 'OTHER', label: 'Other' }
	];

	// State for collapsible sections
	let isCommunityTagsOpen = true;
	let isDegreesOpen = true;
	let isYearsOpen = true; // Added for consistency

	// Selections - now using IDs for consistency with parent filter logic
	let selectedTagIds: number[] = [];
	let selectedDegreeIds: number[] = [];
	let selectedYears: number[] = [];

	// Degree search (internal to sidebar UI)
	let degreeSearchTerm = '';

	// --- Reactive Computations ---

	// Filtered degrees based on search term (uses the 'degrees' prop)
	$: filteredDegrees = degreeSearchTerm.trim() && degrees
		? degrees.filter(d => 
			d.name.toLowerCase().includes(degreeSearchTerm.toLowerCase())
		)
		: degrees;

	// Years of study options
	const yearOptions = [1, 2, 3, 4, 5]; // Assuming up to 5 years, adjust as needed

	// --- Functions ---

	function getActiveQueryParams() {
		const active: Record<string, any> = {};
		
		for (const k in queryParams) {
			const keyCasted = k as keyof typeof queryParams;
			const param = queryParams[keyCasted];
			if (param.enabled) {
				if (keyCasted === 'isPublic') {
					active[param.label] = param.value;
				} else if (param.value !== null && param.value !== '') {
					active[param.label] = param.value;
				}
			}
		}
		
		if (ageRangeEnabled) {
			active['min_age'] = ageMin;
			active['max_age'] = ageMax;
		}
		
		if (participantsRangeEnabled) { // If this filter is relevant to students
			active['min_participants'] = participantsMin;
			active['max_participants'] = participantsMax;
		}

		if (selectedTagIds.length > 0) {
			active['community_tags'] = selectedTagIds; // Parent expects IDs
		}
		if (selectedDegreeIds.length > 0) {
			active['degrees'] = selectedDegreeIds; // Parent expects IDs
		}
		if (selectedYears.length > 0) {
			active['years'] = selectedYears;
		}
		
		return active;
	}

	function dispatchQueryParamChange() {
		dispatch('queryParamsChange', { activeQueryParams: getActiveQueryParams() });
	}

	function clearQueryParams() {
		let changed = false;
		
		for (const k in queryParams) {
			const keyCasted = k as keyof typeof queryParams;
			const p = queryParams[keyCasted];
			if (p.enabled || (p.value !== '' && p.value !== null && p.value !== false)) {
				changed = true;
			}
			p.enabled = false;
			if (keyCasted === 'isPublic') p.value = false;
			else if (keyCasted === 'gender') p.value = '';
		}
		
		if (ageRangeEnabled) { ageRangeEnabled = false; ageMin = 18; ageMax = 65; changed = true; }
		if (participantsRangeEnabled) { participantsRangeEnabled = false; participantsMin = 1; participantsMax = 100; changed = true; }
		
		if (selectedTagIds.length > 0) { selectedTagIds = []; changed = true; }
		if (selectedDegreeIds.length > 0) { selectedDegreeIds = []; changed = true; }
		if (selectedYears.length > 0) { selectedYears = []; changed = true; }

		if (changed) dispatchQueryParamChange();
	}

	function toggleQueryParam(key: keyof typeof queryParams) {
		queryParams[key].enabled = !queryParams[key].enabled;
		dispatchQueryParamChange();
	}

	function toggleAgeRange() {
		ageRangeEnabled = !ageRangeEnabled;
		dispatchQueryParamChange();
	}

	function toggleParticipantsRange() {
		participantsRangeEnabled = !participantsRangeEnabled;
		dispatchQueryParamChange();
	}

	function handleRangeChange() { // Could be used by sliders if any
		dispatchQueryParamChange();
	}

	// Tag selection (using IDs)
	function toggleCommunityTag(tagId: number) {
		selectedTagIds = selectedTagIds.includes(tagId)
			? selectedTagIds.filter((id) => id !== tagId)
			: [...selectedTagIds, tagId];
		// dispatch('communityTagSelectionChange', { selectedTagIds }); // Optional: if parent needs immediate notice of this specific change
		dispatchQueryParamChange();
	}

	function clearAllCommunityTags() {
		if (selectedTagIds.length) {
			selectedTagIds = [];
			dispatchQueryParamChange();
		}
	}

	// Degree selection (using IDs)
	function toggleDegreeSelection(degreeId: number) {
		selectedDegreeIds = selectedDegreeIds.includes(degreeId)
			? selectedDegreeIds.filter(id => id !== degreeId)
			: [...selectedDegreeIds, degreeId];
		dispatchQueryParamChange();
	}

	function clearAllDegrees() {
		if (selectedDegreeIds.length) {
			selectedDegreeIds = [];
			dispatchQueryParamChange();
		}
	}
	
	// Year selection
	function toggleYear(year: number) {
		selectedYears = selectedYears.includes(year)
			? selectedYears.filter((y) => y !== year)
			: [...selectedYears, year];
		dispatchQueryParamChange();
	}

	function clearAllYears() {
		if (selectedYears.length) {
			selectedYears = [];
			dispatchQueryParamChange();
		}
	}

	// Dispatch initial state once props are potentially ready (though onMount might be too early if props are async)
	// Parent should ideally call applyFilter once student data and aux data is loaded.
	// For now, dispatching onMount is fine to set initial empty/default filters.
	onMount(() => {
		dispatchQueryParamChange();
	});

	// Calculate if any filter is active for the "Clear All" button
	$: anyQueryParamEnabled = Object.values(queryParams).some(p => p.enabled) || 
							 ageRangeEnabled || 
							 participantsRangeEnabled || 
							 selectedTagIds.length > 0 || 
							 selectedDegreeIds.length > 0 || 
							 selectedYears.length > 0;

	// Helper to disable controls when parent is loading
	$: controlsDisabled = isLoading; 

</script>

<!-- 
  Tailwind classes added/modified for alignment and behavior:
  - md:w-72 lg:w-80: Defines width on medium and large screens.
  - flex flex-col: Makes the aside a flex container for its children, useful for layout.
  - md:sticky md:top-0 md:h-screen: Makes the sidebar sticky and full-height on desktop.
  - overflow-y-auto: Allows sidebar content to scroll if it overflows.
  - md:flex-shrink-0: Prevents sidebar from shrinking in a flex row on desktop.
-->
<aside class="md:w-72 lg:w-80 bg-gray-900 text-white shadow-lg flex flex-col  md:top-0 md:h-screen overflow-y-auto px-4 py-6 md:flex-shrink-0">
	<div class="mb-6">
		<h2 class="mb-3 text-xl font-bold">Filters</h2>
		<div class="space-y-4"> <!-- Adjusted spacing slightly -->
		
			<!-- Gender -->
			<div class="border border-gray-700 rounded-lg p-3 {queryParams.gender.enabled ? 'bg-gray-800' : 'bg-gray-900'}">
				<div class="flex items-center gap-x-2 mb-2">
					<input
						type="checkbox"
						id="enable-gender"
						bind:checked={queryParams.gender.enabled}
						on:change={() => toggleQueryParam('gender')}
						disabled={controlsDisabled}
						class="form-checkbox h-4 w-4 rounded text-blue-600 bg-gray-700 border-gray-600 focus:ring-blue-500 disabled:opacity-60 disabled:cursor-not-allowed"
					/>
					<label for="enable-gender" class="text-sm font-medium {controlsDisabled ? 'opacity-60' : ''}">Gender</label>
				</div>
				<select
					id="value-gender"
					bind:value={queryParams.gender.value}
					disabled={!queryParams.gender.enabled || controlsDisabled}
					on:change={dispatchQueryParamChange}
					class="w-full rounded bg-gray-700 p-1.5 text-sm border border-gray-600 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-60 disabled:cursor-not-allowed"
				>
					<option disabled value="">Select gender</option>
					{#each genderOptions as opt}
						<option value={opt.value}>{opt.label}</option>
					{/each}
				</select>
			</div>

			<!-- Public Status -->
			<div class="border border-gray-700 rounded-lg p-3 {queryParams.isPublic.enabled ? 'bg-gray-800' : 'bg-gray-900'}">
				<div class="flex items-center gap-x-2">
					<input
						type="checkbox"
						id="enable-isPublic"
						bind:checked={queryParams.isPublic.enabled}
						on:change={() => toggleQueryParam('isPublic')}
						disabled={controlsDisabled}
						class="form-checkbox h-4 w-4 rounded text-blue-600 bg-gray-700 border-gray-600 focus:ring-blue-500 disabled:opacity-60 disabled:cursor-not-allowed"
					/>
					<label for="enable-isPublic" class="text-sm font-medium {controlsDisabled ? 'opacity-60' : ''}">Public Status</label>
					<div class="flex-grow"></div>
					<input
						type="checkbox"
						id="value-isPublic"
						bind:checked={queryParams.isPublic.value}
						disabled={!queryParams.isPublic.enabled || controlsDisabled}
						on:change={dispatchQueryParamChange}
						class="form-checkbox h-4 w-4 rounded text-blue-600 bg-gray-700 border-gray-600 focus:ring-blue-500 disabled:opacity-60 disabled:cursor-not-allowed"
					/>
					<label for="value-isPublic" class="text-sm select-none {(queryParams.isPublic.enabled && !controlsDisabled) ? '' : 'opacity-60'}">Is Public</label>
				</div>
			</div>

            <!-- Age Range -->
            <div class="border border-gray-700 rounded-lg p-3 {ageRangeEnabled ? 'bg-gray-800' : 'bg-gray-900'}">
                <div class="flex items-center gap-x-2 mb-2">
                    <input
                        type="checkbox"
                        id="enable-age-range"
                        bind:checked={ageRangeEnabled}
                        on:change={toggleAgeRange}
                        disabled={controlsDisabled}
                        class="form-checkbox h-4 w-4 rounded text-blue-600 bg-gray-700 border-gray-600 focus:ring-blue-500 disabled:opacity-60 disabled:cursor-not-allowed"
                    />
                    <label for="enable-age-range" class="text-sm font-medium {controlsDisabled ? 'opacity-60' : ''}">Age Range</label>
                </div>
                <div class="flex items-center gap-x-2 text-sm">
                    <input type="number" bind:value={ageMin} min="0" max="150" disabled={!ageRangeEnabled || controlsDisabled} on:input={handleRangeChange} class="w-1/2 rounded bg-gray-700 p-1.5 border border-gray-600 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-60 disabled:cursor-not-allowed" />
                    <span>to</span>
                    <input type="number" bind:value={ageMax} min="0" max="150" disabled={!ageRangeEnabled || controlsDisabled} on:input={handleRangeChange} class="w-1/2 rounded bg-gray-700 p-1.5 border border-gray-600 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-60 disabled:cursor-not-allowed" />
                </div>
                 {#if ageRangeEnabled && ageMin > ageMax}
                    <p class="mt-1 text-xs text-red-400">Min age cannot exceed max age.</p>
                {/if}
            </div>

		</div>
		{#if anyQueryParamEnabled}
			<button 
				on:click={clearQueryParams} 
				disabled={controlsDisabled}
				class="mt-4 w-full rounded bg-red-600 py-2 text-sm font-medium hover:bg-red-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
			>
				Clear All Filters
			</button>
		{/if}
	</div>

	<!-- Community Tags (uses 'tags' prop) -->
	<div class="mb-6">
		<button
			on:click={() => isCommunityTagsOpen = !isCommunityTagsOpen}
			disabled={controlsDisabled}
			class="flex w-full items-center justify-between mb-3 text-xl font-bold hover:text-blue-400 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
			aria-expanded={isCommunityTagsOpen}
			aria-controls="community-tags-content"
		>
			Community Tags
			<span class="transform transition-transform duration-200 {isCommunityTagsOpen ? 'rotate-180' : ''}">▼</span>
		</button>
		{#if isCommunityTagsOpen}
			<div id="community-tags-content">
				{#if !tags || tags.length === 0}
					<p class="text-sm text-gray-400 {controlsDisabled ? 'opacity-60' : ''}">No community tags available.</p>
				{:else}
					<ul class="space-y-1 max-h-60 overflow-y-auto pr-1">
						{#each tags as tag (tag.id)}
							{@const isSelected = selectedTagIds.includes(tag.id)}
							<li>
								<button
									on:click={() => toggleCommunityTag(tag.id)}
									disabled={controlsDisabled}
									class="flex w-full items-center justify-between rounded p-2 text-left text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed {isSelected ? 'bg-blue-700 hover:bg-blue-600' : 'bg-gray-800 hover:bg-gray-700'}"
								>
									<span>{tag.name}</span>
									{#if isSelected}<span class="text-blue-300">✓</span>{/if}
								</button>
							</li>
						{/each}
					</ul>
					{#if selectedTagIds.length > 0}
						<button 
							on:click={clearAllCommunityTags} 
							disabled={controlsDisabled}
							class="mt-3 w-full rounded bg-red-600 py-2 text-sm font-medium hover:bg-red-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed">
							Clear Tags ({selectedTagIds.length})
						</button>
					{/if}
				{/if}
			</div>
		{/if}
	</div>

	<!-- Degrees (uses 'degrees' prop) -->
    <div class="mb-6">
        <button
            on:click={() => isDegreesOpen = !isDegreesOpen}
            disabled={controlsDisabled}
            class="flex w-full items-center justify-between mb-3 text-xl font-bold hover:text-green-400 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
            aria-expanded={isDegreesOpen}
            aria-controls="degrees-content"
        >
            Degrees
            <span class="transform transition-transform duration-200 {isDegreesOpen ? 'rotate-180' : ''}">▼</span>
        </button>
        {#if isDegreesOpen}
            <div id="degrees-content">
                {#if !degrees || degrees.length === 0}
                    <p class="text-sm text-gray-400 {controlsDisabled ? 'opacity-60' : ''}">No degrees available.</p>
                {:else}
                    <div class="mb-2">
                        <input
                            type="text"
                            placeholder="Search degrees..."
                            bind:value={degreeSearchTerm}
                            disabled={controlsDisabled}
                            class="w-full rounded bg-gray-800 p-1.5 text-sm border border-gray-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-60 disabled:cursor-not-allowed"
                        />
                    </div>
                    
                    <ul class="space-y-1 max-h-60 overflow-y-auto pr-1">
                        {#each filteredDegrees as degree (degree.id)}
                            {@const isSelected = selectedDegreeIds.includes(degree.id)}
                            <li>
                                <button
                                    on:click={() => toggleDegreeSelection(degree.id)}
                                    disabled={controlsDisabled}
                                    class="flex w-full items-center justify-between rounded p-2 text-left text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed {isSelected ? 'bg-green-700 hover:bg-green-600' : 'bg-gray-800 hover:bg-gray-700'}"
                                >
                                    <span class="line-clamp-2">{degree.name}</span>
                                    {#if isSelected}<span class="text-green-300 ml-1 flex-shrink-0">✓</span>{/if}
                                </button>
                            </li>
                        {/each}
                        
                        {#if filteredDegrees.length === 0 && degreeSearchTerm.trim() !== ''}
                            <li class="text-sm text-gray-400 p-2 {controlsDisabled ? 'opacity-60' : ''}">No degrees match your search.</li>
                        {/if}
                    </ul>
                    
                    {#if selectedDegreeIds.length > 0}
                        <button 
							on:click={clearAllDegrees} 
							disabled={controlsDisabled}
							class="mt-3 w-full rounded bg-red-600 py-2 text-sm font-medium hover:bg-red-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed">
                            Clear Degrees ({selectedDegreeIds.length})
                        </button>
                    {/if}
                {/if}
            </div>
        {/if}
    </div>

	<!-- Year of Study -->
	<div class="mb-6"> <!-- Consistent mb-6 with other sections -->
		<button
            on:click={() => isYearsOpen = !isYearsOpen}
            disabled={controlsDisabled}
            class="flex w-full items-center justify-between mb-3 text-xl font-bold hover:text-purple-400 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
            aria-expanded={isYearsOpen}
            aria-controls="years-content"
        >
            Year of Study
            <span class="transform transition-transform duration-200 {isYearsOpen ? 'rotate-180' : ''}">▼</span>
        </button>
		{#if isYearsOpen}
			<div id="years-content" class="border border-gray-700 rounded-lg p-3 bg-gray-900"> <!-- Added styling similar to other filters -->
				<ul class="space-y-1">
					{#each yearOptions as year (year)}
						{@const isSelected = selectedYears.includes(year)}
						<li class="flex items-center gap-x-2">
							<input
								type="checkbox"
								id={`year-${year}`}
								checked={isSelected}
								on:change={() => toggleYear(year)}
								disabled={controlsDisabled}
								class="form-checkbox h-4 w-4 rounded text-purple-600 bg-gray-700 border-gray-600 focus:ring-purple-500 disabled:opacity-60 disabled:cursor-not-allowed"
							/>
							<label for={`year-${year}`} class="text-sm select-none {controlsDisabled ? 'opacity-60' : ''}">Year {year}</label>
						</li>
					{/each}
				</ul>
				{#if selectedYears.length > 0}
					<button 
						on:click={clearAllYears} 
						disabled={controlsDisabled}
						class="mt-3 w-full rounded bg-red-600 py-2 text-sm font-medium hover:bg-red-700 transition-colors disabled:opacity-60 disabled:cursor-not-allowed">
						Clear Years ({selectedYears.length})
					</button>
				{/if}
			</div>
		{/if}
	</div>

    <!-- Note: Participants range filter section is omitted as its relevance to students isn't clear from context.
         If needed, it can be added similarly to the Age Range filter. -->

</aside>
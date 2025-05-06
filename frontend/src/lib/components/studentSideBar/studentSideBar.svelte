
<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { get } from '$lib/api/get';

	const dispatch = createEventDispatcher();

	interface Tag {
		name: string;
		originalValue: any;
	}

	interface Degree {
		id: number;
		name: string;
		created_at: number;
		updated_at: number;
	}

	// Age range
	let ageMin = 18;
	let ageMax = 65;
	let ageRangeEnabled = false;
	
	// Participants range
	let participantsMin = 1;
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

	function getActiveQueryParams() {
		const active: Record<string, any> = {};
		
		// Add gender and isPublic if enabled
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
		
		// Add age range if enabled
		if (ageRangeEnabled) {
			active['min_age'] = ageMin;
			active['max_age'] = ageMax;
		}
		
		// Add participants range if enabled
		if (participantsRangeEnabled) {
			active['min_participants'] = participantsMin;
			active['max_participants'] = participantsMax;
		}

		// Add selected tags and degrees
		if (selectedCommunityTags.length > 0) {
			active['community_tags'] = selectedCommunityTags;
		}
		if (selectedDegrees.length > 0) {
			active['degrees'] = selectedDegrees.map(d => d.id);
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
		
		// Reset form controls
		for (const k in queryParams) {
			const keyCasted = k as keyof typeof queryParams;
			const p = queryParams[keyCasted];
			if (p.enabled || (p.value !== '' && p.value !== null && p.value !== false)) {
				changed = true;
			}
			p.enabled = false;
			if (keyCasted === 'isPublic') {
				p.value = false;
			} else if (keyCasted === 'gender') {
				p.value = '';
			}
		}
		
		// Reset range sliders
		if (ageRangeEnabled) {
			ageRangeEnabled = false;
			ageMin = 18;
			ageMax = 65;
			changed = true;
		}
		
		if (participantsRangeEnabled) {
			participantsRangeEnabled = false;
			participantsMin = 1;
			participantsMax = 100;
			changed = true;
		}
		
		// Reset selections
		if (selectedCommunityTags.length > 0) {
			selectedCommunityTags = [];
			changed = true;
		}
		if (selectedDegrees.length > 0) {
			selectedDegrees = [];
			changed = true;
		}
		if (selectedYears.length > 0) {
			selectedYears = [];
			changed = true;
		}

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

	function handleRangeChange() {
		dispatchQueryParamChange();
	}

	let fetchedCommunityTags: Tag[] = [];
	let selectedCommunityTags: string[] = [];
	let isLoadingCommunityTags = true;
	let communityTagsError: string | null = null;

	async function fetchCommunityTags() {
		isLoadingCommunityTags = true;
		communityTagsError = null;
		try {
			const responseData = await get<any>('tags/list/');
			const rawTags = responseData?.tags ?? (Array.isArray(responseData) ? responseData : []);

			fetchedCommunityTags = rawTags
				.map((tagInput: any): Tag | null => {
					if (typeof tagInput === 'string' && tagInput.trim() !== '') {
						return { name: tagInput.trim(), originalValue: tagInput };
					}
					if (tagInput && typeof tagInput === 'object' && typeof tagInput.name === 'string' && tagInput.name.trim() !== '') {
						return { name: tagInput.name.trim(), originalValue: tagInput };
					}
					if (tagInput !== null && tagInput !== undefined) {
            			console.warn('Skipping malformed community tag:', tagInput);
        			}
					return null;
				})
				.filter((tag): tag is Tag => tag !== null);
		} catch (err: any) {
			console.error('Error fetching community tags:', err);
			communityTagsError = `Failed to load community tags: ${err.message || 'Unknown error'}`;
			fetchedCommunityTags = [];
		} finally {
			isLoadingCommunityTags = false;
		}
	}

	function toggleCommunityTag(tag: Tag) {
		selectedCommunityTags = selectedCommunityTags.includes(tag.name)
			? selectedCommunityTags.filter((t) => t !== tag.name)
			: [...selectedCommunityTags, tag.name];
		dispatch('communityTagSelectionChange', { selectedCommunityTags });
		dispatchQueryParamChange();
	}

	function clearAllCommunityTags() {
		if (selectedCommunityTags.length) {
			selectedCommunityTags = [];
			dispatch('communityTagSelectionChange', { selectedCommunityTags });
			dispatchQueryParamChange();
		}
	}

	// Degrees
	let fetchedDegrees: Degree[] = [];
	let selectedDegrees: Degree[] = [];
	let isLoadingDegrees = true;
	let degreesError: string | null = null;
	let degreeSearchTerm = '';

	async function fetchDegrees() {
		isLoadingDegrees = true;
		degreesError = null;
		try {
			const responseData = await get<any>('degrees/list/');
			
			if (responseData?.success && Array.isArray(responseData.degrees)) {
				fetchedDegrees = responseData.degrees;
			} else {
				fetchedDegrees = [];
				console.warn('Unexpected degree data format:', responseData);
			}
		} catch (err: any) {
			console.error('Error fetching degrees:', err);
			degreesError = `Failed to load degrees: ${err.message || 'Unknown error'}`;
			fetchedDegrees = [];
		} finally {
			isLoadingDegrees = false;
		}
	}

	function toggleDegreeSelection(degree: Degree) {
		const isDegreeSelected = selectedDegrees.some(d => d.id === degree.id);
		
		selectedDegrees = isDegreeSelected
			? selectedDegrees.filter(d => d.id !== degree.id)
			: [...selectedDegrees, degree];
			
		dispatch('degreeSelectionChange', { selectedDegrees });
		dispatchQueryParamChange();
	}

	function clearAllDegrees() {
		if (selectedDegrees.length) {
			selectedDegrees = [];
			dispatch('degreeSelectionChange', { selectedDegrees });
			dispatchQueryParamChange();
		}
	}

	// Filtered degrees based on search term
	$: filteredDegrees = degreeSearchTerm.trim() 
		? fetchedDegrees.filter(d => 
			d.name.toLowerCase().includes(degreeSearchTerm.toLowerCase())
		)
		: fetchedDegrees;

	const years = [1, 2, 3, 4];
	let selectedYears: number[] = [];

	function toggleYear(year: number) {
		selectedYears = selectedYears.includes(year)
			? selectedYears.filter((y) => y !== year)
			: [...selectedYears, year];
		dispatch('yearSelectionChange', { selectedYears });
		dispatchQueryParamChange();
	}

	function clearAllYears() {
		if (selectedYears.length) {
			selectedYears = [];
			dispatch('yearSelectionChange', { selectedYears });
			dispatchQueryParamChange();
		}
	}

	onMount(async () => {
		await Promise.all([fetchCommunityTags(), fetchDegrees()]);
		dispatchQueryParamChange();
		dispatch('communityTagSelectionChange', { selectedCommunityTags });
		dispatch('degreeSelectionChange', { selectedDegrees });
		dispatch('yearSelectionChange', { selectedYears });
	});

	$: anyQueryParamEnabled = Object.values(queryParams).some(p => p.enabled) || 
							 ageRangeEnabled || 
							 participantsRangeEnabled || 
							 selectedCommunityTags.length > 0 || 
							 selectedDegrees.length > 0 || 
							 selectedYears.length > 0;
</script>

<aside class="fixed top-0 left-0 h-full w-72 overflow-y-auto bg-gray-900 px-4 py-6 text-white shadow-lg">
	<div class="mb-6">
		<h2 class="mb-3 text-xl font-bold">Filters</h2>
		<div class="space-y-5">
			<!-- Age Range Slider -->
			<div class="border border-gray-700 rounded-lg p-3 {ageRangeEnabled ? 'bg-gray-800' : 'bg-gray-900'}">
				<div class="flex items-center justify-between mb-3">
					<div class="flex items-center gap-x-2">
						<input
							type="checkbox"
							id="enable-age-range"
							bind:checked={ageRangeEnabled}
							on:change={toggleAgeRange}
							class="form-checkbox h-4 w-4 rounded text-blue-600 bg-gray-700 border-gray-600 focus:ring-blue-500"
						/>
						<label for="enable-age-range" class="text-sm font-medium">Age Range</label>
					</div>
					<span class="text-sm font-medium text-blue-400">{ageMin} - {ageMax}</span>
				</div>
				
				<div class="flex gap-4 mb-2">
					<div class="w-1/2">
						<label for="age-min" class="block text-xs text-gray-400 mb-1">Min</label>
						<input
							type="number"
							id="age-min"
							bind:value={ageMin}
							min="18"
							max={ageMax - 1}
							on:change={handleRangeChange}
							disabled={!ageRangeEnabled}
							class="w-full rounded bg-gray-700 p-1 text-sm border border-gray-600 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-50"
						/>
					</div>
					<div class="w-1/2">
						<label for="age-max" class="block text-xs text-gray-400 mb-1">Max</label>
						<input
							type="number"
							id="age-max"
							bind:value={ageMax}
							min={ageMin + 1}
							max="65"
							on:change={handleRangeChange}
							disabled={!ageRangeEnabled}
							class="w-full rounded bg-gray-700 p-1 text-sm border border-gray-600 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-50"
						/>
					</div>
				</div>
				
				<input 
					type="range"
					class="range-primary w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer {ageRangeEnabled ? 'opacity-100' : 'opacity-50'}"
					min="18"
					max="65"
					step="1"
					bind:value={ageMin}
					on:input={() => {
						if (ageMin >= ageMax) ageMax = ageMin + 1;
						handleRangeChange();
					}}
					disabled={!ageRangeEnabled}
				/>
			</div>

		

			<!-- Gender -->
			<div class="border border-gray-700 rounded-lg p-3 {queryParams.gender.enabled ? 'bg-gray-800' : 'bg-gray-900'}">
				<div class="flex items-center gap-x-2 mb-2">
					<input
						type="checkbox"
						id="enable-gender"
						bind:checked={queryParams.gender.enabled}
						on:change={() => toggleQueryParam('gender')}
						class="form-checkbox h-4 w-4 rounded text-blue-600 bg-gray-700 border-gray-600 focus:ring-blue-500"
					/>
					<label for="enable-gender" class="text-sm font-medium">Gender</label>
				</div>
				<select
					id="value-gender"
					bind:value={queryParams.gender.value}
					disabled={!queryParams.gender.enabled}
					on:change={dispatchQueryParamChange}
					class="w-full rounded bg-gray-700 p-1.5 text-sm border border-gray-600 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 disabled:opacity-50"
				>
					<option disabled value="">Select gender</option>
					{#each genderOptions as opt}
						<option value={opt.value}>{opt.label}</option>
					{/each}
				</select>
			</div>

			<!-- Public -->
			<div class="border border-gray-700 rounded-lg p-3 {queryParams.isPublic.enabled ? 'bg-gray-800' : 'bg-gray-900'}">
				<div class="flex items-center gap-x-2">
					<input
						type="checkbox"
						id="enable-isPublic"
						bind:checked={queryParams.isPublic.enabled}
						on:change={() => toggleQueryParam('isPublic')}
						class="form-checkbox h-4 w-4 rounded text-blue-600 bg-gray-700 border-gray-600 focus:ring-blue-500"
					/>
					<label for="enable-isPublic" class="text-sm font-medium">Public Status</label>
					<div class="flex-grow"></div>
					<input
						type="checkbox"
						id="value-isPublic"
						bind:checked={queryParams.isPublic.value}
						disabled={!queryParams.isPublic.enabled}
						on:change={dispatchQueryParamChange}
						class="form-checkbox h-4 w-4 rounded text-blue-600 bg-gray-700 border-gray-600 focus:ring-blue-500 disabled:opacity-50"
					/>
					<label for="value-isPublic" class="text-sm select-none {queryParams.isPublic.enabled ? '' : 'opacity-50'}">Public</label>
				</div>
			</div>
		</div>
		{#if anyQueryParamEnabled}
			<button on:click={clearQueryParams} class="mt-4 w-full rounded bg-red-600 py-2 text-sm font-medium hover:bg-red-700 transition-colors">
				Clear All Filters & Selections
			</button>
		{/if}
	</div>

	<!-- Community Tags -->
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
				{#if isLoadingCommunityTags}
					<div class="flex justify-center py-4"><div class="h-6 w-6 animate-spin rounded-full border-t-2 border-b-2 border-blue-500"></div></div>
				{:else if communityTagsError}
					<p class="rounded-md bg-red-800 p-3 text-sm">{communityTagsError}</p>
				{:else if !fetchedCommunityTags || !fetchedCommunityTags.length}
					<p class="text-sm text-gray-400">No community tags available.</p>
				{:else}
					<ul class="space-y-1 max-h-60 overflow-y-auto pr-1">
						{#each fetchedCommunityTags as tag (tag.name)}
							{@const isSelected = selectedCommunityTags.includes(tag.name)}
							<li>
								<button
									on:click={() => toggleCommunityTag(tag)}
									class="flex w-full items-center justify-between rounded p-2 text-left text-sm transition-colors {isSelected ? 'bg-blue-700 hover:bg-blue-600' : 'bg-gray-800 hover:bg-gray-700'}"
								>
									<span>{tag.name}</span>
									{#if isSelected}<span class="text-blue-300">✓</span>{/if}
								</button>
							</li>
						{/each}
					</ul>
					{#if selectedCommunityTags.length}
						<button on:click={clearAllCommunityTags} class="mt-3 w-full rounded bg-red-600 py-2 text-sm font-medium hover:bg-red-700 transition-colors">
							Clear Tags ({selectedCommunityTags.length})
						</button>
					{/if}
				{/if}
			</div>
		{/if}
	</div>

	<!-- Degrees (Always visible) -->
    <div class="mb-6">
        <button
            on:click={() => isDegreesOpen = !isDegreesOpen}
            class="flex w-full items-center justify-between mb-3 text-xl font-bold hover:text-green-400 transition-colors"
            aria-expanded={isDegreesOpen}
            aria-controls="degrees-content"
        >
            Degrees
            <span class="transform transition-transform duration-200 {isDegreesOpen ? 'rotate-180' : ''}">▼</span>
        </button>
        {#if isDegreesOpen}
            <div id="degrees-content">
                {#if isLoadingDegrees}
                    <div class="flex justify-center py-4"><div class="h-6 w-6 animate-spin rounded-full border-t-2 border-b-2 border-green-500"></div></div>
                {:else if degreesError}
                    <p class="rounded-md bg-red-800 p-3 text-sm">{degreesError}</p>
                {:else if !fetchedDegrees || !fetchedDegrees.length}
                    <p class="text-sm text-gray-400">No degrees available.</p>
                {:else}
                    <!-- Search box for degrees -->
                    <div class="mb-2">
                        <input
                            type="text"
                            placeholder="Search degrees..."
                            bind:value={degreeSearchTerm}
                            class="w-full rounded bg-gray-800 p-1.5 text-sm border border-gray-700 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                        />
                    </div>
                    
                    <!-- List of degrees -->
                    <ul class="space-y-1 max-h-60 overflow-y-auto pr-1">
                        {#each filteredDegrees as degree (degree.id)}
                            {@const isSelected = selectedDegrees.some(d => d.id === degree.id)}
                            <li>
                                <button
                                    on:click={() => toggleDegreeSelection(degree)}
                                    class="flex w-full items-center justify-between rounded p-2 text-left text-sm transition-colors {isSelected ? 'bg-green-700 hover:bg-green-600' : 'bg-gray-800 hover:bg-gray-700'}"
                                >
                                    <span class="line-clamp-2">{degree.name}</span>
                                    {#if isSelected}<span class="text-green-300 ml-1 flex-shrink-0">✓</span>{/if}
                                </button>
                            </li>
                        {/each}
                        
                        {#if filteredDegrees.length === 0 && degreeSearchTerm.trim() !== ''}
                            <li class="text-sm text-gray-400 p-2">No degrees match your search.</li>
                        {/if}
                    </ul>
                    
                    {#if selectedDegrees.length}
                        <button on:click={clearAllDegrees} class="mt-3 w-full rounded bg-red-600 py-2 text-sm font-medium hover:bg-red-700 transition-colors">
                            Clear Degrees ({selectedDegrees.length})
                        </button>
                    {/if}
                {/if}
            </div>
        {/if}
    </div>

	<!-- Year of Study -->
	<div class="border border-gray-700 rounded-lg p-3">
		<h2 class="mb-3 text-lg font-bold">Year of Study</h2>
		<ul class="space-y-1">
			{#each years as year (year)}
				{@const isSelected = selectedYears.includes(year)}
				<li class="flex items-center gap-x-2">
					<input
						type="checkbox"
						id={`year-${year}`}
						checked={isSelected}
						on:change={() => toggleYear(year)}
						class="form-checkbox h-4 w-4 rounded text-purple-600 bg-gray-700 border-gray-600 focus:ring-purple-500"
					/>
					<label for={`year-${year}`} class="text-sm select-none">Year {year}</label>
				</li>
			{/each}
		</ul>
		{#if selectedYears.length}
			<button on:click={clearAllYears} class="mt-3 w-full rounded bg-red-600 py-2 text-sm font-medium hover:bg-red-700 transition-colors">
				Clear Years ({selectedYears.length})
			</button>
		{/if}
	</div>
</aside>
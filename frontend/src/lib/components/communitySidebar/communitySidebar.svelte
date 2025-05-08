
<script lang="ts">

	import SearchBox from '$components/SearchBox/searchBox.svelte';

	// Define data structures
	export let tags: [string, number][] = [];
	export let degree: [string, number][] = [];
	export let ageTo = '';
	export let is_with = 0; // Only When Logged In [0 - All Communities | 1 - User With Community | 2 - User Not With Community]
	export let public_community = 0; //0 - All Communities | 1 - Public Community | 2 - Private Community
	
	// Options for dropdowns
	const membershipOptions = [
		{ value: 0, label: 'All Communities' },
		{ value: 1, label: 'Communities I\'m In' },
		{ value: 2, label: 'Communities I\'m Not In' }
	];
	
	const visibilityOptions = [
		{ value: 0, label: 'All Communities' },
		{ value: 1, label: 'Public Communities' },
		{ value: 2, label: 'Private Communities' }
	];
	
	// Toggle states for new dropdowns
	let isMembershipOpen = true;
	let isVisibilityOpen = true;
	
	// Toggle functions for new dropdowns
	function toggleMembership() {
		isMembershipOpen = !isMembershipOpen;
	}
	
	function toggleVisibility() {
		isVisibilityOpen = !isVisibilityOpen;
	}

	// Toggle states
	let isCommunityTagsOpen = true;
	let isDegreeOpen = true;
	let isMemberOpen = true;


	// Toggle sections
	function toggleCommunityTags() {
		isCommunityTagsOpen = !isCommunityTagsOpen;
	}

	function toggleDegree() {
		isDegreeOpen = !isDegreeOpen;
	}
	
	function toggleMemberOpen() {
		isMemberOpen = !isMemberOpen;
	}
	
	function handleAgeToChange() {
		// Validate the input range if needed
		if (parseInt(ageTo) < 1) ageTo = '1';
		if (parseInt(ageTo) > 999) ageTo = '999';
	}

</script>

<aside class="fixed top-20 left-0 bottom-0 w-72 overflow-y-auto bg-gray-900 px-4 py-6 text-black shadow-lg">
	<div class="mb-6">
		<h2 class="mb-3 text-xl font-bold text-white">Filters</h2>
		
		<!-- Community Tags with Search -->
		<div class="mb-6">
			<div class="flex items-center justify-between">
				<button 
					class="flex items-center text-lg font-semibold"
					on:click={toggleCommunityTags}
				>
					<span class="text-white">Community Tags</span>
				</button>
			</div>

			{#if isCommunityTagsOpen}
				<div class="mt-2">
					<SearchBox
						id="tags"
						classStyle="w-full bg-gray-800 border border-gray-700 rounded-lg p-2 focus:outline-none focus:border-blue-500 text-white"
						marginTop=""
						placeholder="Search for Tags..."
						url="tags/list/"
						multi_select={true}
						max_select={5}
						bind:selected={tags}
					/>
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
					<span class="text-white">Degree</span>
				</button>
			</div>
			{#if isDegreeOpen}
				<div class="mt-2">
					<SearchBox
						id="degree"
						classStyle="w-full bg-gray-800 border border-gray-700 rounded-lg p-2 focus:outline-none focus:border-blue-500 text-white"
						marginTop=""
						placeholder="Search for Degree..."
						url="degrees/list/"
						multi_select={false}
						bind:selected={degree}
					/>
				</div>
			{/if}
		</div>

		<div class="mb-6">
			<div class="flex items-center justify-between">
				<button 
					class="flex items-center text-lg font-semibold"
					on:click={toggleMemberOpen}
				>
					<span class="text-white">Min Memebers</span>
				</button>
			</div>
			{#if isMemberOpen}
				<div class="mt-2">
					<div class="w-full bg-gray-800 border border-gray-700 rounded-lg p-2 text-white">
						<div class="flex items-center gap-3 mb-2">
							<label class="w-1/2">
								<input 
									type="number" 
									min="1" 
									max="999" 
									class="w-full bg-gray-700 border border-gray-600 rounded px-2 py-1 text-white focus:outline-none focus:border-blue-500" 
									bind:value={ageTo} 
									on:change={handleAgeToChange}
								/>
							</label>
						</div>
					</div>
				</div>
			{/if}
		</div>

		<!-- Membership Filter -->
		<div class="mb-6">
			<div class="flex items-center justify-between">
				<button 
					class="flex items-center text-lg font-semibold"
					on:click={toggleMembership}
				>
					<span class="text-white">Membership Status</span>
				</button>
			</div>
			{#if isMembershipOpen}
				<div class="mt-2">
					<div class="w-full bg-gray-800 border border-gray-700 rounded-lg p-2 text-white">
						{#each membershipOptions as option}
							<div class="flex items-center gap-2 py-1">
								<input 
									type="radio" 
									id="membership-{option.value}" 
									name="membership" 
									value={option.value} 
									bind:group={is_with}
									class="accent-blue-500"
								/>
								<label for="membership-{option.value}">{option.label}</label>
							</div>
						{/each}
					</div>
				</div>
			{/if}
		</div>

		<!-- Visibility Filter -->
		<div class="mb-6">
			<div class="flex items-center justify-between">
				<button 
					class="flex items-center text-lg font-semibold"
					on:click={toggleVisibility}
				>
					<span class="text-white">Community Visibility</span>
				</button>
			</div>
			{#if isVisibilityOpen}
				<div class="mt-2">
					<div class="w-full bg-gray-800 border border-gray-700 rounded-lg p-2 text-white">
						{#each visibilityOptions as option}
							<div class="flex items-center gap-2 py-1">
								<input 
									type="radio" 
									id="visibility-{option.value}" 
									name="visibility" 
									value={option.value} 
									bind:group={public_community}
									class="accent-blue-500"
								/>
								<label for="visibility-{option.value}">{option.label}</label>
							</div>
						{/each}
					</div>
				</div>
			{/if}
		</div>
	</div>
</aside>

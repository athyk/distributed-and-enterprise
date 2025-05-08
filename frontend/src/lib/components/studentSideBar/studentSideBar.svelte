<script lang="ts">
	import SearchBox from '$components/SearchBox/searchBox.svelte';

	// Define data structures
	export let tags: [string, number][] = [];
	export let degree: [string, number][] = [];
	export let ageFrom: string = ''; // Added minimum age
	export let ageTo: string = ''; // Added maximum age

	// Toggle states
	let isStudentTagsOpen = true; // Renamed from isCommunityTagsOpen to isStudentTagsOpen
	let isDegreeOpen = true;
	let isAgeRangeOpen = true;

	// Toggle sections
	function toggleStudentTags() {
		isStudentTagsOpen = !isStudentTagsOpen;
	}

	function toggleDegree() {
		isDegreeOpen = !isDegreeOpen;
	}

	function toggleAgeRange() {
		isAgeRangeOpen = !isAgeRangeOpen;
	}

	// Handle age range changes
	function handleAgeFromChange(event) {
		ageFrom = event.target.value;
	}

	function handleAgeToChange(event) {
		ageTo = event.target.value;
	}
</script>

<aside
	class="fixed top-20 bottom-0 left-0 w-72 overflow-y-auto bg-gray-900 px-4 py-6 text-black shadow-lg"
>
	<div class="mb-6">
		<h2 class="mb-3 text-xl font-bold text-white">Filters</h2>

		<!-- Student Tags with Search (renamed from Community Tags) -->
		<div class="mb-6">
			<div class="flex items-center justify-between">
				<button class="flex items-center text-lg font-semibold" on:click={toggleStudentTags}>
					<span class="text-white">Student Tags</span>
				</button>
			</div>

			{#if isStudentTagsOpen}
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
				<button class="flex items-center text-lg font-semibold" on:click={toggleDegree}>
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

		<!-- Age Range Filter (NEW) -->
		<div class="mb-6">
			<div class="flex items-center justify-between">
				<button class="flex items-center text-lg font-semibold" on:click={toggleAgeRange}>
					<span class="text-white">Age Range</span>
				</button>
			</div>
			{#if isAgeRangeOpen}
				<div class="mt-2">
					<div class="w-full rounded-lg border border-gray-700 bg-gray-800 p-2 text-white">
						<div class="mb-2 flex items-center gap-3">
							<label class="w-1/2">
								<span class="mb-1 block text-sm">From</span>
								<input
									type="number"
									min="18"
									max="100"
									class="w-full rounded border border-gray-600 bg-gray-700 px-2 py-1 text-white focus:border-blue-500 focus:outline-none"
									bind:value={ageFrom}
									on:change={handleAgeFromChange}
								/>
							</label>
							<label class="w-1/2">
								<span class="mb-1 block text-sm">To</span>
								<input
									type="number"
									min="18"
									max="100"
									class="w-full rounded border border-gray-600 bg-gray-700 px-2 py-1 text-white focus:border-blue-500 focus:outline-none"
									bind:value={ageTo}
									on:change={handleAgeToChange}
								/>
							</label>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</div>
</aside>

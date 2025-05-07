
<script lang="ts">

	import SearchBox from '$components/SearchBox/searchBox.svelte';

	// Define data structures
	export let tags: [string, number][] = [];
	export let degree: [string, number][] = [];

	// Toggle states
	let isCommunityTagsOpen = true;
	let isDegreeOpen = true;


	// Toggle sections
	function toggleCommunityTags() {
		isCommunityTagsOpen = !isCommunityTagsOpen;
	}

	function toggleDegree() {
		isDegreeOpen = !isDegreeOpen;
	}
</script>

<aside class="fixed top-16 left-0 bottom-0 w-72 overflow-y-auto bg-gray-900 px-4 py-6 text-black shadow-lg">
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
	</div>
</aside>

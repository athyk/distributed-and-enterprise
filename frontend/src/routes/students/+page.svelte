<script lang="ts">
	import StudentCard from '$lib/components/studentCard/studentCard.svelte';
	import Sidebar from '$lib/components/studentSideBar/studentSideBar.svelte';
	import { get } from '$lib/api/get';
	import Popup from '$components/ErrorPopUp/popup.svelte';
	import type { StudentSearchResponse, studentData } from '$lib/api/apiType';
	import Tags from '$components/Post/Sections/tags.svelte';
	import { getDegreeName } from '$lib/api/getDegreeID';
	import { getTagName } from '$lib/api/getTagID';
	import { onMount } from 'svelte';

	let tags: [string, number][] = [];
	let degree: [string, number][] = [];
	let gender: [string, number][] = []; // Match the sidebar's data structure
	let ageFrom: string = "";
	let ageTo: string = "";
	export let year: string;

	function removeTag(tag: [string, number]) {
		tags = tags.filter(t => t[1] !== tag[1]);
	}

	function clearAllTags() {
		tags = [];
	}

	function buildQueryString() {
		let query = '';

		if (tags.length > 0) {
			query += tags.map(tag => `tag_id=${tag[1]}`).join('&') ;
		}

		if (degree.length > 0) {
			query += '&'
			query += degree.map(deg => `degree_id=${deg[1]}`).join('&') ;
		}

		// Add gender filter if selected
		if (gender.length > 0 && gender[0]) {
			query += `&gender=${gender[0]}`;
		}

		// Add age range filters if provided
		if (ageFrom) {
			query += `&age_from=${ageFrom}&`;
		}

		if (ageTo) {
			query += `&age_to=${ageTo}&`;
		}

		if (searchQuery) {
			query += `&first_name=${searchQuery}`;
		}

		// Remove trailing '&' if it exists
		if (query.endsWith('&')) {
			query = query.slice(0, -1);
		}

		return query;
	}


	async function fetchStudents() {
		console.log('Fetching students with query:', searchQuery);
		error = '';

		const queryString = buildQueryString();
		console.log('Query string:', queryString);

		try {
			// Add a question mark to properly format the URL with query parameters
			const apiUrl = queryString ? `users/?${queryString}` : 'users/';
			const response = (await get(apiUrl)) as StudentSearchResponse;
			console.log('Response:', response);
			filteredStudents = response.users || [];
		} catch (err) {
			error = 'Failed to fetch students. Please try again later.';
			console.error('Error fetching students:', err);
			return;
		}
	}

$: if (tags.length > 0 || searchQuery || degree.length > 0 || gender.length > 0 || ageFrom || ageTo) {
	fetchStudents();
}

	let searchQuery: string = '';
	let filteredStudents: studentData[] = [];
	let error: string = '';

	onMount(() => {
		fetchStudents();
	});
</script>

<!-- Component Layout -->
<Popup bind:errorMessage={error} />
<div class="flex min-h-screen bg-gray-50">
	<!-- Sidebar Component with all necessary bindings -->
     <Sidebar bind:tags={tags} bind:degree={degree} bind:gender={gender} bind:ageFrom={ageFrom} bind:ageTo={ageTo} /> 
	<!-- Main Content -->
	<div class="ml-64 flex-1 p-6"> <!-- Adjust ml-64 if sidebar width changes -->
		<div class="mx-auto max-w-6xl">
			<!-- Header with Search Bar -->
	<!-- Header with Search Bar -->
<div class="mb-8 flex flex-col items-center gap-4"> <!-- Removed justify-between and sm:flex-row -->
    <!-- Search Bar Section -->
    <div class="flex w-full max-w-lg items-center gap-2 rounded-full border border-gray-300 bg-white p-2 px-3 shadow-sm focus-within:ring-2 focus-within:ring-blue-500 focus-within:ring-offset-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
        </svg>
        <input
            type="text"
            bind:value={searchQuery}
            placeholder="Search for a student..."
            class="w-full flex-1 bg-transparent px-2 text-gray-900 outline-none"
        />
      
   
    </div>
</div>

			<!-- Active Filters Display -->
			{#if tags.length > 0}
				<div class="mb-6 flex flex-wrap items-center gap-2 rounded-lg border border-gray-200 bg-white p-3 shadow-sm">
					<span class="text-sm font-medium text-gray-600">Active filters:</span>
					{#each tags as tag (tag[1])}
						<span class="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-sm font-medium text-blue-800">
							{tag[0]}
							<button
								class="ml-1.5 -mr-1 flex-shrink-0 rounded-full p-0.5 inline-flex items-center justify-center text-blue-500 hover:bg-blue-200 hover:text-blue-700 focus:outline-none focus:bg-blue-200"
								aria-label={`Remove ${tag[0]} filter`}
								on:click={() => removeTag(tag)}
							>
                                <svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                                    <path stroke-linecap="round" stroke-width="1.5" d="M1 1l6 6 m0-6L1 7" />
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

			<!-- Display Loading, Error, or Students -->
			{#if filteredStudents.length === 0} <!-- Show loading spinner only on initial load or when list is empty -->
			<div class="flex flex-col items-center justify-center py-12 text-center">
				<!-- Example: Magnifying glass icon (Heroicons) -->
				<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 text-gray-400 dark:text-gray-500 mb-3">
					<path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
				</svg>
				<p class="text-md font-medium text-gray-700 dark:text-gray-300">
					Ready to find a student?
				</p>
				<p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
					Enter a name or apply filters to see results.
				</p>
			</div>
			{:else if error}
				<div class="rounded-lg border border-red-200 bg-red-50 p-4 text-center text-red-700 shadow-sm">
					<h3 class="font-medium">Oops! Something went wrong.</h3>
					<p class="text-sm mt-1">{error}</p>
					<button
						on:click={() => fetchStudents()}
						class="mt-3 inline-flex items-center rounded-md border border-transparent bg-red-100 px-3 py-1.5 text-sm font-medium text-red-700 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:ring-offset-red-50"
					>
						Try Again
					</button>
				</div>
			{:else}
				{#if filteredStudents.length > 0}
					<div class="grid w-full grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
						{#each filteredStudents as student (student.id)}
							<StudentCard
								userId={student.id}
								firstName={student.first_name}
								lastName={student.last_name}
								tagNames={student.tags}
								degreeName={String(student.degree_id)}
								gender={student.gender || 'N/A'}
								dateOfBirth={student.date_of_birth}
								yearOfStudy={student.year_of_study || 'N/A'}
								gradDate={student.grad_date || ''}
							/>
						{/each}
					</div>
				{:else}
					<!-- Improved "No Results" Message -->
					<div class="flex flex-col items-center justify-center rounded-lg border border-gray-200 bg-white p-8 text-center shadow-sm min-h-[200px]">
						<svg class="h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 10a.01.01 0 01.01-.01M10 10a.01.01 0 00-.01-.01m.01.01H10m0 0v.01M10 10a.01.01 0 01.01.01m0 0a.01.01 0 00-.01.01m0-.01H10m0 0V9.99m0 .01a.01.01 0 00.01-.01m-.01.01H10m0 0V9.99"></path></svg>
						<h3 class="text-lg font-medium text-gray-800">No Students Found</h3>
						<p class="mt-1 text-sm text-gray-500">
							{#if searchQuery || tags.length > 0}
								Try adjusting your search or filters.
							{:else}
								There are currently no students listed.
							{/if}
						</p>
					</div>
				{/if}
			{/if}
		</div>
	</div>
</div>

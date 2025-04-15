
<script lang="ts">
	import { onMount } from 'svelte';
	import StudentCard from '$lib/components/studentCard/studentCard.svelte';
	import { get } from '$lib/api/get';

	// --- Type Definitions ---
	interface Tag {
		id: number;
		name: string;
	}

	interface Student {
		id: number;
		email: string;
		first_name: string;
		last_name: string;
		gender: string;
		date_of_birth: string;
		picture_url: string;
		degree_id: number;
		year_of_study: number;
		grad_date: string;
		tags: number[];
	}

	interface ProcessedStudent extends Omit<Student, 'tags'> {
		tags: Tag[];
		degreeName: string;
	}

	// --- Component State ---
	let searchQuery: string = '';
	let students: ProcessedStudent[] = [];
	let filteredStudents: ProcessedStudent[] = [];
	let isLoading: boolean = true;
	let error: string | null = null;

	// Define a map for degree IDs to names
	const degreeMap: Record<number, string> = {
		94: 'Computer Science',
		95: 'Data Science',
		96: 'Business Administration'
	};

	// Define a map for tag IDs to names
	const tagMap: Record<number, string> = {
		17: 'Programming',
		24: 'Web Development',
		55: 'AI',
		109: 'Data Science',
		157: 'Machine Learning'
	};

	// --- Debounce Timer Reference ---
	let debounceTimer: number;

	// --- Fetch Function ---
	async function fetchStudents(): Promise<void> {
		isLoading = true;
		error = null;
		console.log('[fetchStudents] Fetching student data');

		try {
			const response = await get<any>('users/');
			console.log('[fetchStudents] Raw API Response Data:', response);

			let studentsData: Student[] = [];

			// --- Adjust based on your actual API response structure ---
			if (Array.isArray(response)) {
				studentsData = response;
			} else if (response.students && Array.isArray(response.students)) {
				studentsData = response.students;
			} else if (response.users && Array.isArray(response.users)) {
				studentsData = response.users;
			} else if (response.results && Array.isArray(response.results)) {
				studentsData = response.results;
			} else if (response.data && Array.isArray(response.data)) {
				studentsData = response.data;
			} else {
				throw new Error('Unexpected API response format. Expected an array of students.');
			}

			console.log('[fetchStudents] Identified Students Data:', studentsData);

			// Process and map students
			students = studentsData.map(student => {
				// Map tag IDs to tag objects with names
				const processedTags = Array.isArray(student.tags)
					? student.tags.map(tagId => ({
							id: tagId,
							name: tagMap[tagId] || `Tag ${tagId}`
					  }))
					: [];

				return {
					...student,
					degreeName: degreeMap[student.degree_id] || `Degree ${student.degree_id}`,
					tags: processedTags
				};
			});

			console.log('[fetchStudents] Processed Students:', students);

			// Apply initial filter (empty search = show all)
			applySearch('');
		} catch (err: any) {
			console.error('[fetchStudents] Failed to fetch students:', err);
			error = err instanceof Error ? err.message : 'Failed to load students. Please try again later.';
			students = [];
			filteredStudents = [];
		} finally {
			isLoading = false;
			console.log('[fetchStudents] Fetch complete. isLoading:', isLoading);
		}
	}

	// --- Apply Search Function ---
	function applySearch(query: string = ''): void {
		console.log(`[applySearch] Applying search with query: "${query}"`);
		
		filteredStudents = students.filter(student => {
			// Filter by search query (name match)
			if (!query) return true;
			
			const fullName = `${student.first_name} ${student.last_name}`.toLowerCase();
			const searchLower = query.toLowerCase();
			
			return fullName.includes(searchLower);
		});
		
		console.log('[applySearch] Filtered Students Count:', filteredStudents.length);
	}

	// --- Debounced Search Function ---
	function debouncedSearch(): void {
		clearTimeout(debounceTimer);
		console.log('[debouncedSearch] Input detected, setting timeout.');
		debounceTimer = window.setTimeout(() => {
			console.log(`[debouncedSearch] Timeout finished. Applying search with query "${searchQuery}"`);
			applySearch(searchQuery);
		}, 300);
	}

	// --- Explicit Search Function ---
	function handleSearchClick(): void {
		clearTimeout(debounceTimer);
		console.log(`[handleSearchClick] Search button clicked. Applying search with query "${searchQuery}"`);
		applySearch(searchQuery);
	}

	// --- Clear Search Function ---
	function clearSearch(): void {
		searchQuery = '';
		applySearch('');
	}

	// --- Initial Data Load ---
	onMount(() => {
		console.log('[onMount] Component mounted. Fetching students data.');
		fetchStudents();
	});
</script>

<main class="container mx-auto px-4 py-4">
	<h1 class="mb-6 text-3xl font-bold text-gray-900 dark:text-white">Student Directory</h1>
	
	<!-- Search Bar Section -->
	<div class="mb-8 flex justify-center">
		<div class="flex w-full max-w-2xl items-center gap-2 rounded-full border border-gray-300 bg-white p-3 shadow-sm">
			<input
				type="text"
				bind:value={searchQuery}
				placeholder="Search by student name..."
				class="w-full bg-transparent px-4 text-gray-900 outline-none"
				on:input={debouncedSearch}
				on:keydown={(e) => { if (e.key === 'Enter') handleSearchClick(); }}
			/>
			{#if searchQuery}
				<button
					on:click={clearSearch}
					class="rounded-full p-2 text-gray-500 hover:bg-gray-100"
					aria-label="Clear search"
				>
					<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
					</svg>
				</button>
			{/if}
			<button
				on:click={handleSearchClick}
				class="rounded-full bg-blue-500 px-6 py-2 text-white shadow-md transition hover:bg-blue-600 disabled:opacity-50"
				disabled={isLoading}
			>
				{isLoading ? 'Loading...' : 'Search'}
			</button>
		</div>
	</div>
	
	<!-- Display Loading, Error, or Students -->
	{#if isLoading}
		<div class="flex justify-center py-12">
			<div class="animate-spin h-10 w-10 border-4 border-blue-500 rounded-full border-t-transparent"></div>
		</div>
	{:else if error}
		<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
			<strong class="font-bold">Error:</strong>
			<span class="block sm:inline"> {error}</span>
			<button 
				class="mt-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
				on:click={fetchStudents}
			>
				Retry
			</button>
		</div>
	{:else if filteredStudents.length > 0}
		<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
			{#each filteredStudents as student (student.id)}
				<StudentCard
					firstName={student.first_name}
					lastName={student.last_name}
					gender={student.gender}
					dateOfBirth={student.date_of_birth}
					pictureUrl={student.picture_url}
					degreeId={student.degree_id}
					degreeName={student.degreeName}
					yearOfStudy={student.year_of_study}
					gradDate={student.grad_date}
					tags={student.tags.map(t => t.id)}
					tagNames={student.tags.map(t => t.name)}
				/>
			{/each}
		</div>
	{:else}
		<div class="text-center py-8">
			<p class="text-lg text-gray-500">No students found matching your search criteria.</p>
			{#if searchQuery}
				<button 
					class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
					on:click={clearSearch}
				>
					Clear Search
				</button>
			{:else}
				<button 
					class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
					on:click={fetchStudents}
				>
					Refresh
				</button>
			{/if}
		</div>
	{/if}
	
	<!-- Debug section - Remove in production -->
	{#if import.meta.env.DEV}
		<div class="mt-10 p-4 border border-gray-300 rounded bg-gray-50">
			<h3 class="text-lg font-semibold mb-2">Debug Information:</h3>
			<p>Loading state: {isLoading ? 'Loading...' : 'Finished'}</p>
			<p>Error: {error || 'None'}</p>
			<p>Search query: "{searchQuery}"</p>
			<p>Total students: {students.length}</p>
			<p>Filtered students: {filteredStudents.length}</p>
			<details>
				<summary class="cursor-pointer text-blue-600">View filtered students data</summary>
				<pre class="mt-2 p-2 bg-gray-100 overflow-auto max-h-96">{JSON.stringify(filteredStudents, null, 2)}</pre>
			</details>
		</div>
	{/if}
</main>
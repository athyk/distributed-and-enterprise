<script lang="ts">
	import { onMount } from 'svelte';
	import StudentCard from '$lib/components/studentCard/studentCard.svelte';
	import { get } from '$lib/api/get';

	// --- Constants ---
	const DEBOUNCE_DELAY = 300;
	// Using HARDCODED maps again as requested
	const DEGREE_MAP: Record<number, string> = {
		94: 'Computer Science',
		95: 'Data Science',
		96: 'Business Administration',
		// Add more as needed
	};
	const TAG_MAP: Record<number, string> = {
		17: 'Programming',
		24: 'Web Development',
		55: 'AI',
		109: 'Data Science',
		157: 'Machine Learning',
		// Add more as needed
	};
	const STUDENT_API_URL = 'users/'; // Assuming relative path works with base URL in 'get' util

	// --- Type Definitions ---
	interface Tag {
		id: number;
		name: string;
	}
	// ApiDegree type is no longer needed as we're not fetching degrees

	// Raw student data structure from API
	interface ApiStudent {
		id: number;
		email: string;
		first_name: string;
		last_name: string;
		gender: string;
		date_of_birth: string;
		picture_url: string;
		degree_id: number; // Keep original degree_id
		year_of_study: number;
		grad_date: string;
		tags: number[]; // Assuming API sends tag IDs
	}

	// Processed student data structure used in the component
	// No longer needs to Omit degree_id if StudentCard needs it
	interface DisplayStudent extends Omit<ApiStudent, 'tags'> {
		degreeName: string; // Added processed degree name
		displayTags: Tag[]; // Renamed for clarity
	}

	// --- Component State ---
	let searchQuery = '';
	let allStudents: DisplayStudent[] = []; // Stores the full list after fetch
	let filteredStudents: DisplayStudent[] = []; // Stores the list to display
	let isLoading = true; // Single loading state for students
	let error: string | null = null; // Single error state for students
	let debounceTimer: ReturnType<typeof setTimeout>;

	// --- Data Fetching & Processing ---
	async function fetchStudents(): Promise<void> {
		isLoading = true;
		error = null;
		allStudents = [];
		filteredStudents = [];

		try {
			// STEP 1: Fetch students
			console.log("Fetching students...");
			const response = await get<unknown>(STUDENT_API_URL);

			// Robust checking for the student array
			let rawStudents: ApiStudent[];
			if (typeof response === 'object' && response !== null) {
				if (Array.isArray((response as any).students)) rawStudents = (response as any).students;
				else if (Array.isArray((response as any).users)) rawStudents = (response as any).users;
				else if (Array.isArray((response as any).results)) rawStudents = (response as any).results;
				else if (Array.isArray(response)) rawStudents = response as ApiStudent[];
				else throw new Error('Unexpected student API response format (object but no known array key)');
			} else if (Array.isArray(response)) {
				rawStudents = response as ApiStudent[];
			} else {
				throw new Error('Unexpected student API response format (not object or array)');
			}

			console.log(`Fetched ${rawStudents.length} raw students. Processing...`);

			// STEP 2: Process students using the CONSTANT maps
			allStudents = rawStudents.map((stu: ApiStudent): DisplayStudent | null => {
				try {
					// Use CONSTANT TAG_MAP
					const displayTags: Tag[] = Array.isArray(stu.tags)
						? stu.tags
								.map((id) => ({ id, name: TAG_MAP[id] }))
								.filter((tag): tag is Tag => tag.name !== undefined)
						: [];

					// Use CONSTANT DEGREE_MAP
					const degreeName = DEGREE_MAP[stu.degree_id] ?? `Unknown Degree (ID: ${stu.degree_id})`;

					// Keep all original fields except 'tags' (which is replaced by displayTags)
					// We still need degree_id if StudentCard uses it
					// eslint-disable-next-line @typescript-eslint/no-unused-vars
					const { tags, ...rest } = stu; // Keep degree_id in 'rest'

					// Basic validation
					if (typeof stu.id !== 'number' || !stu.first_name || !stu.last_name) {
						 console.warn("Skipping student due to missing essential data:", stu);
						 return null;
					}

					return {
						...rest, // includes degree_id now
						degreeName,
						displayTags,
					};
				} catch(processingError) {
					 console.error("Error processing individual student:", stu, processingError);
					 return null;
				}
			}).filter((student): student is DisplayStudent => student !== null);

			console.log(`Processed ${allStudents.length} valid students.`);

			// STEP 3: Initialize filtered list
			applyFilter();

		} catch (e: unknown) {
			console.error('Failed during student data loading process:', e);
			error = e instanceof Error ? e.message : 'An unknown error occurred while loading students.';
			allStudents = [];
			filteredStudents = [];
		} finally {
			isLoading = false;
			console.log("Student loading finished.");
		}
	}

	// --- Filtering Logic ---
	function applyFilter(): void {
		const query = searchQuery.trim().toLowerCase();
		if (!query) {
			filteredStudents = [...allStudents];
			return;
		}
		// Ensure student processing finished before filtering
		if (isLoading || error) return;

		filteredStudents = allStudents.filter((student) =>
			!student ? false :
			`${student.first_name} ${student.last_name}`.toLowerCase().includes(query) ||
			student.degreeName.toLowerCase().includes(query) ||
			student.displayTags.some(tag => tag.name.toLowerCase().includes(query))
		);
	}

	// --- Event Handlers ---
	function handleSearchInput(): void {
		clearTimeout(debounceTimer);
		debounceTimer = setTimeout(applyFilter, DEBOUNCE_DELAY);
	}

	function handleImmediateSearch(): void {
		clearTimeout(debounceTimer);
		applyFilter();
	}

	function handleClearSearch(): void {
		searchQuery = '';
		applyFilter();
	}

	function handleRetryFetch(): void {
		fetchStudents(); // Retry fetching students
	}

	// --- Lifecycle ---
	onMount(() => {
		fetchStudents(); // Start fetching students
	});

</script>

<main class="container mx-auto min-h-screen px-4 py-8">
	<h1 class="mb-8 text-center text-3xl font-bold text-gray-800 md:text-4xl">Student Directory</h1>

	<div class="mb-10 flex justify-center">
		<div
			class="flex w-full max-w-xl items-center gap-2 rounded-full border border-gray-300 bg-white p-2 px-4 shadow-sm focus-within:ring-2 focus-within:ring-blue-500 focus-within:ring-opacity-50"
		>
			<span class="text-gray-400">
				<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
			</span>
			<input
				type="text"
				bind:value={searchQuery}
				on:input={handleSearchInput}
				on:keydown={(e) => e.key === 'Enter' && handleImmediateSearch()}
				placeholder="Search by name, degree, or tag..."
				class="flex-grow bg-transparent py-1 text-gray-700 placeholder-gray-400 outline-none"
				aria-label="Search students"
				disabled={isLoading || !!error}
			/>
			{#if searchQuery}
				<button
					on:click={handleClearSearch}
					aria-label="Clear search"
					class="flex items-center justify-center rounded-full p-1 text-gray-500 hover:bg-gray-100"
					type="button"
				>
					<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
				</button>
			{/if}
		</div>
	</div>

	<div class="py-8">
		{#if isLoading}
			<div class="flex flex-col items-center justify-center space-y-4 text-gray-500" role="status">
				<div
					class="h-12 w-12 animate-spin rounded-full border-4 border-solid border-blue-500 border-t-transparent"
				></div>
				<span class="text-lg font-medium">Loading Students...</span>
			</div>
		{:else if error}
			<div
				class="mx-auto max-w-md rounded-lg border border-red-400 bg-red-50 p-6 text-center shadow"
				role="alert"
			>
				<div class="mb-4 flex justify-center text-red-500">
				   <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
				</div>
				<h3 class="mb-2 text-xl font-semibold text-red-800">Oops! Something went wrong.</h3>
				<p class="mb-6 text-red-700">{error}</p>
				<button
					on:click={handleRetryFetch}
					class="rounded-md bg-red-600 px-6 py-2 font-semibold text-white shadow transition hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
				>
					Retry
				</button>
			</div>
		{:else if filteredStudents.length > 0}
			<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
				{#each filteredStudents as student (student.id)}
					<StudentCard
						firstName={student.first_name}
						lastName={student.last_name}
						gender={student.gender}
						dateOfBirth={student.date_of_birth}
						pictureUrl={student.picture_url}
						degreeName={student.degreeName}
						degreeId={student.degree_id} 
						yearOfStudy={student.year_of_study}
						gradDate={student.grad_date}
						tagNames={student.displayTags.map((t) => t.name)}
						tags={student.displayTags.map((t) => t.id)}
					/>
				{/each}
			</div>
		{:else}
			<div class="flex flex-col items-center justify-center space-y-4 py-16 text-center text-gray-500">
				<svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
					<path stroke-linecap="round" stroke-linejoin="round" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
				  </svg>
				<h3 class="text-2xl font-semibold">No Students Found</h3>
				{#if searchQuery}
					<p>Your search for "{searchQuery}" didn't match any students.</p>
					 {#if allStudents.length > 0}
						<button
							on:click={handleClearSearch}
							class="mt-4 rounded-md bg-blue-600 px-5 py-2 font-semibold text-white shadow transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
						>
							Clear Search & Show All
						</button>
					{/if}
				{:else}
					 <p>There are currently no students in the directory.</p>
				{/if}
			</div>
		{/if}
	</div>
</main>
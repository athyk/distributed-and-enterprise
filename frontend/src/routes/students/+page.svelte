
<script lang="ts">
	import { onMount } from 'svelte';
	import StudentCard from '$lib/components/studentCard/studentCard.svelte';
	import StudentSidebar from '$lib/components/studentSideBar/studentSideBar.svelte'; // Make sure this path is correct
	import { get } from '$lib/api/get';

	const DEBOUNCE_DELAY = 300;
	const STUDENT_API_URL = 'users/';
	const DEGREES_API_URL = 'degrees/list/'; // API endpoint for degrees
	const TAGS_API_URL = 'tags/list/';     // API endpoint for tags

	interface Tag {
		id: number;
		name: string;
	}

	interface ApiStudent {
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
		public?: boolean;
	}

	interface DisplayStudent extends Omit<ApiStudent, 'tags'> {
		degreeName: string;
		displayTags: Tag[];
		age?: number;
	}

	interface ApiMapItem {
		id: number; // ID field
		name: string; // Name field
		// Additional properties your API might return
		[key: string]: any;
	}

	let searchQuery = '';
	let allStudents: DisplayStudent[] = [];
	let filteredStudents: DisplayStudent[] = [];
	let isLoading = true;
	let error: string | null = null;
	let debounceTimer: ReturnType<typeof setTimeout>;

	// Maps for degree and tag data
	let degreeMap: Record<number, string> = {};
	let tagMap: Record<number, string> = {};

	// Structured data for sidebar
	let degrees: { id: number, name: string }[] = [];
	let tags: { id: number, name: string }[] = [];

	// Filter state from sidebar
	let activeQueryParams: Record<string, any> = {};

	// Handle filter changes from the sidebar
	function handleQueryParamsChange(event: CustomEvent) {
		activeQueryParams = event.detail.activeQueryParams;
		console.log('Filter parameters updated:', activeQueryParams);
		applyFilter();
	}

	// Fetch degrees and tags data
	// Fetch degrees and tags data
async function fetchAuxiliaryData(): Promise<void> {
    console.log('Fetching auxiliary data (degrees and tags)...');
    try {
        const [degreesResponse, tagsResponse] = await Promise.all([
            get<unknown>(DEGREES_API_URL),
            get<unknown>(TAGS_API_URL)
        ]);

        // --- Process Degrees ---
        let rawDegreesArray: ApiMapItem[] = [];
        if (degreesResponse && typeof degreesResponse === 'object' && 'degrees' in degreesResponse && Array.isArray((degreesResponse as any).degrees)) {
            rawDegreesArray = (degreesResponse as any).degrees;
        } else if (Array.isArray(degreesResponse)) {
            rawDegreesArray = degreesResponse as ApiMapItem[];
        } else {
            console.warn(`Unexpected format for degrees response. Expected Object with 'degrees' array or direct Array.`);
        }

        degrees = []; // For sidebar
        degreeMap = {}; // For mapping
        rawDegreesArray.forEach(item => {
            if (typeof item.id === 'number' && typeof item.name === 'string') {
                degrees.push({ id: item.id, name: item.name });
                degreeMap[item.id] = item.name;
            } else {
                console.warn('Skipping degree item due to invalid format:', item);
            }
        });
        console.log('Processed Degree Map:', degreeMap);
        console.log('Processed Degrees for Sidebar:', degrees);

        // --- Process Tags ---
        let rawTagsArray: ApiMapItem[] = [];
        if (tagsResponse && typeof tagsResponse === 'object' && 'tags' in tagsResponse && Array.isArray((tagsResponse as any).tags)) {
            rawTagsArray = (tagsResponse as any).tags;
        } else if (Array.isArray(tagsResponse)) {
            rawTagsArray = tagsResponse as ApiMapItem[];
        } else {
            console.warn(`Unexpected format for tags response. Expected Object with 'tags' array or direct Array.`);
        }

        tags = []; // For sidebar
        tagMap = {}; // For mapping
        rawTagsArray.forEach(item => {
            // Crucially, we expect each tag item to have an 'id' and 'name'
            if (typeof item.id === 'number' && typeof item.name === 'string') {
                tags.push({ id: item.id, name: item.name });
                tagMap[item.id] = item.name;
            } else {
                console.warn('Skipping tag item due to invalid format (missing id or name):', item);
            }
        });
        console.log('Processed Tag Map:', tagMap);
        console.log('Processed Tags for Sidebar:', tags);

    } catch (e) {
        console.error('Failed to load degrees or tags:', e);
        if (!error) {
            error = e instanceof Error ? `Auxiliary data error: ${e.message}` : 'Failed to load filter options.';
        }
        degrees = [];
        tags = [];
        degreeMap = {};
        tagMap = {};
    }
}

	// Fetch student data
	async function fetchStudents(): Promise<void> {
		isLoading = true;
		error = null;
		allStudents = [];
		filteredStudents = [];

		try {
			await fetchAuxiliaryData(); // Ensure maps are populated first

			console.log("Fetching students...");
			const response = await get<unknown>(STUDENT_API_URL);

			let rawStudents: ApiStudent[];
			if (Array.isArray(response)) {
				rawStudents = response as ApiStudent[];
			} else if (typeof response === 'object' && response !== null) {
				if (Array.isArray((response as any).students)) rawStudents = (response as any).students;
				else if (Array.isArray((response as any).users)) rawStudents = (response as any).users;
				else if (Array.isArray((response as any).results)) rawStudents = (response as any).results;
				else throw new Error('Unexpected API response: object does not contain a known student array key.');
			} else {
				throw new Error('Unexpected API response: data is not an array or a recognized object structure.');
			}

			console.log(`Fetched ${rawStudents.length} raw students. Processing...`);

			allStudents = rawStudents.map((stu: ApiStudent): DisplayStudent | null => {
				try {
					const displayTags: Tag[] = Array.isArray(stu.tags)
						? stu.tags
								.map((id) => ({ id, name: tagMap[id] || `Unknown Tag (ID: ${id})` }))
						: [];

					const degreeName = degreeMap[stu.degree_id] ?? `Unknown Degree (ID: ${stu.degree_id})`;

					// eslint-disable-next-line @typescript-eslint/no-unused-vars
					const { tags, ...rest } = stu;

					if (typeof stu.id !== 'number' || !stu.first_name || !stu.last_name) {
						 console.warn("Skipping student due to missing essential data:", stu);
						 return null;
					}

					let age: number | undefined = undefined;
					if (stu.date_of_birth) {
						const dob = new Date(stu.date_of_birth);
						const today = new Date();
						age = today.getFullYear() - dob.getFullYear();
						const monthDiff = today.getMonth() - dob.getMonth();
						if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
							age--;
						}
					}

					return {
						...rest,
						degreeName,
						displayTags,
						age
					};
				} catch(processingError) {
					 console.error("Error processing individual student:", stu, processingError);
					 return null;
				}
			}).filter((student): student is DisplayStudent => student !== null);

			console.log(`Processed ${allStudents.length} valid students.`);
			applyFilter();

		} catch (e: unknown) {
			console.error('Failed during student data loading process:', e);
			error = error || (e instanceof Error ? e.message : 'An unknown error occurred while loading students.');
			allStudents = [];
			filteredStudents = [];
		} finally {
			isLoading = false;
			console.log("Student loading finished.");
		}
	}

	// Apply all filters to the student data
	function applyFilter(): void {
		if (error && !allStudents.length) {
			filteredStudents = [];
			return;
		}

		const query = searchQuery.trim().toLowerCase();

		filteredStudents = allStudents.filter((student) => {
			// Text search filter
			const matchesSearchQuery = !query || (
				`${student.first_name} ${student.last_name}`.toLowerCase().includes(query) ||
				student.degreeName.toLowerCase().includes(query) ||
				student.displayTags.some(tag => tag.name.toLowerCase().includes(query))
			);
			if (!matchesSearchQuery) return false;

			// Age range filter
			if (activeQueryParams.min_age !== undefined && student.age !== undefined) {
				if (student.age < activeQueryParams.min_age) return false;
			}
			
			if (activeQueryParams.max_age !== undefined && student.age !== undefined) {
				if (student.age > activeQueryParams.max_age) return false;
			}
			
			// Gender filter
			if (activeQueryParams.gender && student.gender) {
				if (student.gender.toLowerCase() !== activeQueryParams.gender.toLowerCase()) return false;
			}
			
			// Public status filter
			if (activeQueryParams.public !== undefined && student.public !== undefined) {
				if (student.public !== activeQueryParams.public) return false;
			}
			
			// Degree filter
			if (activeQueryParams.degrees && activeQueryParams.degrees.length > 0) {
				if (!activeQueryParams.degrees.includes(student.degree_id)) return false;
			}
			
			// Community tags filter
			if (activeQueryParams.community_tags && activeQueryParams.community_tags.length > 0) {
				const studentTagIds = student.displayTags.map(tag => tag.id);
				const hasAnyTag = activeQueryParams.community_tags.some((tagId: number) => 
					studentTagIds.includes(tagId)
				);
				if (!hasAnyTag) return false;
			}
			
			// Year of study filter
			if (activeQueryParams.years && activeQueryParams.years.length > 0) {
				if (!activeQueryParams.years.includes(student.year_of_study)) return false;
			}

			return true; // Student passed all filters
		});

		console.log(`Filtered students: ${filteredStudents.length} out of ${allStudents.length}`);
	}

	// Handle search input with debounce
	function handleSearchInput(): void {
		clearTimeout(debounceTimer);
		debounceTimer = setTimeout(applyFilter, DEBOUNCE_DELAY);
	}

	// Immediately apply search filter (for Enter key)
	function handleImmediateSearch(): void {
		clearTimeout(debounceTimer);
		applyFilter();
	}

	// Clear search input
	function handleClearSearch(): void {
		searchQuery = '';
		applyFilter();
	}

	// Retry data fetching
	function handleRetryFetch(): void {
		fetchStudents();
	}

	// Initialize on component mount
	onMount(() => {
		fetchStudents();
	});
</script>

<div class="flex flex-col md:flex-row min-h-screen bg-gray-100">
    <!-- StudentSideBar component with props for degrees, tags, and loading state -->
    <StudentSidebar 
        on:queryParamsChange={handleQueryParamsChange}
        degrees={degrees}
        tags={tags}
        isLoading={isLoading}
    />

    <div class="flex-1 md:overflow-y-auto">
        <main class="container mx-auto px-4 py-8"> 
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
                        disabled={isLoading || (!!error && !allStudents.length)}
                    />
                    {#if searchQuery}
                        <button
                            on:click={handleClearSearch}
                            aria-label="Clear search term"
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
                {:else if error && !allStudents.length}
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
                        {#if allStudents.length === 0 && !isLoading}
                            <p>There are currently no students in the directory.</p>
                        {:else}
                            <p>
                                No students match your current filter criteria.
                                {#if searchQuery && Object.values(activeQueryParams).some(val => Array.isArray(val) ? val.length > 0 : val !== undefined && val !== '')}
                                    Try adjusting your search term "{searchQuery}" or your selected filters.
                                {:else if searchQuery}
                                    Try adjusting your search term "{searchQuery}".
                                {:else if Object.values(activeQueryParams).some(val => Array.isArray(val) ? val.length > 0 : val !== undefined && val !== '')}
                                    Try adjusting your selected filters.
                                {/if}
                            </p>
                        {/if}
                    </div>
                {/if}
            </div>
        </main>
    </div>
</div>

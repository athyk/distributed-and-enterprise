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
	let searchQuery = '';
	let students: ProcessedStudent[] = [];
	let filteredStudents: ProcessedStudent[] = [];
	let isLoading = true;
	let error: string | null = null;
  
	// --- Degree & Tag Maps ---
	const degreeMap: Record<number, string> = {
	  94: 'Computer Science',
	  95: 'Data Science',
	  96: 'Business Administration'
	};
	const tagMap: Record<number, string> = {
	  17: 'Programming',
	  24: 'Web Development',
	  55: 'AI',
	  109: 'Data Science',
	  157: 'Machine Learning'
	};
  
	// --- Debounce Reference ---
	let debounceTimer: ReturnType<typeof setTimeout>;
  
	// --- Fetch & Process Students ---
	async function fetchStudents(): Promise<void> {
	  isLoading = true;
	  error = null;
	  try {
		const response = await get<any>('users/');
		// unify potential array sources
		const raw =
		  (Array.isArray(response) && response) ||
		  response.students ||
		  response.users ||
		  response.results ||
		  response.data ||
		  [];
		if (!Array.isArray(raw)) {
		  throw new Error('Unexpected API response format');
		}
		students = raw.map((stu: Student) => {
		  const tags: Tag[] = Array.isArray(stu.tags)
			? stu.tags.map(id => ({ id, name: tagMap[id] ?? `Tag ${id}` }))
			: [];
		  return {
			...stu,
			degreeName: degreeMap[stu.degree_id] ?? `Degree ${stu.degree_id}`,
			tags
		  };
		});
		// initialize filtered list
		filteredStudents = [...students];
	  } catch (e: unknown) {
		error = e instanceof Error ? e.message : String(e);
		students = [];
		filteredStudents = [];
	  } finally {
		isLoading = false;
	  }
	}
  
	// --- Filtering Logic ---
	function filterStudents(): void {
	  const q = searchQuery.trim().toLowerCase();
	  if (!q) {
		filteredStudents = [...students];
		return;
	  }
	  filteredStudents = students.filter(s =>
		`${s.first_name} ${s.last_name}`.toLowerCase().includes(q)
	  );
	}
  
	// --- Reactive Debounce on Search ---
	$: if (searchQuery !== undefined) {
	  clearTimeout(debounceTimer);
	  debounceTimer = setTimeout(filterStudents, 300);
	}
  
	function clearSearch(): void {
	  searchQuery = '';
	  filterStudents();
	}
  
	// --- On Mount ---
	onMount(fetchStudents);
  </script>
  
  <main class="container mx-auto px-4 py-4">
	<h1 class="mb-6 text-3xl font-bold">Student Directory</h1>
  
	<!-- Search Bar -->
	<div class="mb-8 flex justify-center">
	  <div class="flex w-full max-w-2xl items-center gap-2 rounded-full border p-3 shadow-sm">
		<input
		  type="text"
		  bind:value={searchQuery}
		  placeholder="Search by student name..."
		  class="w-full bg-transparent px-4 outline-none"
		  on:keydown={(e) => e.key === 'Enter' && clearTimeout(debounceTimer) && filterStudents()}
		/>
		{#if searchQuery}
		  <button on:click={clearSearch} aria-label="Clear search" class="p-2">
			✕
		  </button>
		{/if}
		<button
		  on:click={() => { clearTimeout(debounceTimer); filterStudents(); }}
		  class="px-6 py-2 rounded-full bg-blue-500 text-white shadow-md disabled:opacity-50"
		  disabled={isLoading}
		>
		  {isLoading ? 'Loading...' : 'Search'}
		</button>
	  </div>
	</div>
  
	<!-- State Displays -->
	{#if isLoading}
	  <div class="flex justify-center py-12">
		<div class="animate-spin h-10 w-10 border-4 border-t-transparent rounded-full"></div>
	  </div>
	{:else if error}
	  <div class="alert-error p-4 rounded">
		<strong>Error:</strong> {error}
		<button on:click={fetchStudents} class="mt-2 px-4 py-2 bg-red-500 text-white rounded">Retry</button>
	  </div>
	{:else if filteredStudents.length}
	  <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
		{#each filteredStudents as s (s.id)}
		  <StudentCard
			firstName={s.first_name}
			lastName={s.last_name}
			gender={s.gender}
			dateOfBirth={s.date_of_birth}
			pictureUrl={s.picture_url}
			degreeName={s.degreeName}
			yearOfStudy={s.year_of_study}
			gradDate={s.grad_date}
			tags={s.tags.map(t => t.id)}
			tagNames={s.tags.map(t => t.name)}
		  />
		{/each}
	  </div>
	{:else}
	  <div class="text-center py-8">
		<p>No students found.</p>
		<button on:click={clearSearch} class="mt-4 px-4 py-2 bg-blue-500 text-white rounded">Clear Search</button>
	  </div>
	{/if}
  </main>
  
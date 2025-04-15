
<script lang="ts">
	export let firstName: string;
	export let lastName: string;
	export let gender: string;
	export let dateOfBirth: string;
	export let pictureUrl: string = '';
	export let degreeId: number;
	export let degreeName: string = 'Not specified'; // This would come from mapping the degree_id to a name
	export let yearOfStudy: number;
	export let gradDate: string;
	export let tags: number[] = [];
	export let tagNames: string[] = []; // This would come from mapping the tag IDs to names
</script>

<div class="mx-auto max-w-2xl space-y-4 rounded-xl bg-white p-6 shadow-lg dark:bg-gray-900">
	<!-- Header with Student Name -->
	<div class="flex flex-col items-center justify-between border-b pb-4 md:flex-row">
		<div class="flex items-center">
			{#if pictureUrl}
				<img src={pictureUrl} alt="Profile" class="mr-4 h-12 w-12 rounded-full object-cover" />
			{:else}
				<div class="mr-4 flex h-12 w-12 items-center justify-center rounded-full bg-gray-200 text-xl font-bold text-gray-600">
					{firstName.charAt(0)}{lastName.charAt(0)}
				</div>
			{/if}
			<h2 class="text-2xl font-bold text-gray-900 dark:text-white">
				{firstName} {lastName}
			</h2>
		</div>
		<div class="mt-4 md:mt-0">
			<!-- Connect Button -->
			<button
				class="rounded bg-blue-600 px-4 py-2 font-semibold text-white transition hover:bg-blue-700"
			>
				Connect +
			</button>
		</div>
	</div>

	<!-- Student Info -->
	<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
		<div>
			<p class="text-sm font-medium text-gray-500 dark:text-gray-400">Gender</p>
			<p class="text-gray-700 dark:text-gray-300">{gender}</p>
		</div>
		<div>
			<p class="text-sm font-medium text-gray-500 dark:text-gray-400">Date of Birth</p>
			<p class="text-gray-700 dark:text-gray-300">{dateOfBirth}</p>
		</div>
		<div>
			<p class="text-sm font-medium text-gray-500 dark:text-gray-400">Degree</p>
			<p class="text-gray-700 dark:text-gray-300">{degreeName}</p>
		</div>
		<div>
			<p class="text-sm font-medium text-gray-500 dark:text-gray-400">Year of Study</p>
			<p class="text-gray-700 dark:text-gray-300">{yearOfStudy}</p>
		</div>
	</div>

	<!-- Expected Graduation -->
	<div>
		<p class="text-sm font-medium text-gray-500 dark:text-gray-400">Expected Graduation</p>
		<p class="text-gray-700 dark:text-gray-300">{gradDate}</p>
	</div>

	<!-- Tags/Interests -->
	{#if tagNames && tagNames.length > 0}
		<div>
			<p class="mb-2 text-sm font-medium text-gray-500 dark:text-gray-400">Interests</p>
			<div class="flex flex-wrap gap-2">
				{#each tagNames as tag}
					<span
						class="rounded-full bg-gray-200 px-3 py-1 text-sm text-gray-700 dark:bg-gray-800 dark:text-gray-200"
					>
						{tag}
					</span>
				{/each}
			</div>
		</div>
	{/if}

	<!-- Bottom Row: Study Info -->
	<div class="flex items-center justify-between border-t pt-4 text-gray-600 dark:text-gray-400">
		<div class="flex items-center space-x-2">
			<span class="text-lg font-bold text-gray-900 dark:text-white">Year {yearOfStudy}</span>
			<span class="text-sm">Student</span>
		</div>
		<div class="text-sm">
			Graduates in {new Date(gradDate).getFullYear()}
		</div>
	</div>
</div>
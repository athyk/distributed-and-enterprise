<script lang="ts">
	import { goto } from '$app/navigation'; // For SvelteKit navigation

	import {getTagName} from '$lib/api/getTagID';
	import { getDegreeName } from '$lib/api/getDegreeID';

	// --- Component Props ---
	export let userId: string; // This will be the '6' in '/user/6'
	export let pictureUrl: string | null = null;
	export let firstName: string = 'Default';
	export let lastName: string = 'User';
	export let gender: string = 'N/A';
	export let dateOfBirth: string | null = null; // e.g., "1995-08-15"
	export let degreeName: string = 'Not Specified';
	export let yearOfStudy: number | string = 'N/A';
	export let gradDate: string; // e.g., "2025-05-20T00:00:00Z"
	export let tagNames: string[] = [];

	// --- Helper Functions ---
	const formatDate = (dateString: string): string => {
		if (!dateString) return 'N/A';
		try {
			return new Date(dateString).toLocaleDateString(undefined, {
				year: 'numeric',
				month: 'long',
				day: 'numeric'
			});
		} catch (e) {
			return 'Invalid Date';
		}
	};

	$: age = (() => {
		if (!dateOfBirth) return 'N/A';
		try {
			const birthDate = new Date(dateOfBirth);
			const today = new Date();
			let calculatedAge = today.getFullYear() - birthDate.getFullYear();
			const m = today.getMonth() - birthDate.getMonth();
			if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
				calculatedAge--;
			}
			return calculatedAge >= 0 ? calculatedAge : 'N/A';
		} catch (e) {
			return 'N/A';
		}
	})();

	// --- Navigation Logic ---
	const targetUrl = `/user/${userId}`; // Construct the target URL

	function handleCardClick() {
		goto(targetUrl); // Navigate using SvelteKit's goto
	}

	// Accessibility: Allow keyboard navigation (Enter/Space)
	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault(); // Prevent space from scrolling page
			handleCardClick();
		}
	}
</script>

<!--
  Outermost div is now clickable and acts like a button.
  - `on:click`: Triggers navigation.
  - `role="button"`: Accessibility hint.
  - `tabindex="0"`: Makes it keyboard focusable.
  - `on:keydown`: Handles Enter/Space key presses.
  - `cursor-pointer`, `hover:shadow-md`, `focus:ring-2`: UX enhancements.
-->
<div
	class="flex w-full cursor-pointer flex-col space-y-4 rounded-lg border border-gray-200 bg-white p-4 min-h-80 transition-shadow duration-150 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
	on:click={handleCardClick}
	on:keydown={handleKeyDown}
	role="button"
	tabindex="0"
	aria-label={`View details for ${firstName} ${lastName}`}
>
	<!-- Header -->
	<div class="flex items-center">
		{#if pictureUrl}
			<img
				src={pictureUrl}
				alt="Profile of {firstName} {lastName}"
				class="mr-3 h-10 w-10 flex-shrink-0 rounded-full object-cover"
			/>
		{:else}
			<div
				class="mr-3 flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-gray-100 text-lg font-semibold text-gray-700"
				aria-hidden="true"
			>
				{firstName?.charAt(0) || ''}{lastName?.charAt(0) || ''}
			</div>
		{/if}
		<h2 class="truncate text-xl font-bold text-gray-900">
			{firstName} {lastName}
		</h2>
	</div>

	<!-- Student Info Grid -->
	<div class="grid grid-cols-1 gap-x-4 gap-y-2 md:grid-cols-2">
		<div>
			<p class="text-sm font-medium text-gray-500">Gender</p>
			<p class="font-semibold text-gray-800">{gender}</p>
		</div>
		<div>
			<p class="text-sm font-medium text-gray-500">Age</p>
			<p class="font-semibold text-gray-800">{age}</p>
		</div>
		<div>
			<p class="text-sm font-medium text-gray-500">Degree</p>
			{#await getDegreeName(degreeName.toString()) then degreeConverted}
				<span class="rounded-md bg-gray-100 px-2.5 py-0.5 text-sm font-semibold text-gray-800">{degreeConverted}</span>
			{:catch error}
				<span class="bg-red-200 rounded-md px-2 py-1 text-sm">Error</span>
			{/await}
		</div>
		<div>
			<p class="text-sm font-medium text-gray-500">Year of Study</p>
			<p class="font-semibold text-gray-800">{yearOfStudy}</p>
		</div>
	</div>

	<!-- Expected Graduation -->
	<div>
		<p class="text-sm font-medium text-gray-500">Expected Graduation</p>
		<p class="font-semibold text-gray-800">{formatDate(gradDate)}</p>
	</div>

	<!-- Tags/Interests -->
	{#if tagNames && tagNames.length > 0}
		<div class="flex-grow">
			<p class="mb-1 text-sm font-medium text-gray-500">Tags</p>
			<div class="flex flex-wrap gap-2">
				{#each tagNames as tag}
					{#await getTagName(tag.toString()) then tagName}
					<span class="rounded-md bg-gray-100 px-2.5 py-0.5 text-sm font-semibold text-gray-800">
						{tagName}
					</span>
					{:catch error}
					<span class="rounded-md bg-red-200 px-2.5 py-0.5 text-sm font-semibold text-gray-800">
						Error
					</span>
					{/await}
				{/each}
			</div>
		</div>
	{:else}
        <!-- Ensures bottom row stays down even if no tags -->
		<div class="flex-grow" />
	{/if}

	<!-- Bottom Row -->
	<div class="mt-auto flex items-center justify-between pt-2 text-sm text-gray-600">
		<div class="flex items-center space-x-2">
			<span class="text-base font-bold text-gray-900">Year {yearOfStudy}</span>
			<span class="text-gray-500">Student</span>
		</div>
		<div class="font-semibold">
			{#if gradDate}
				Graduates in {new Date(gradDate).getFullYear()}
			{:else}
				Graduation Year N/A
			{/if}
		</div>
	</div>
</div>
<script lang="ts">
	export let name: string;
	export let isPublic: boolean;
	export let description: string;
	export let tags: string[];
	export let degrees: string[];
	export let totalMembers: number;
	export let creationDate: string;
</script>

<div class="mx-auto max-w-2xl space-y-4 rounded-xl bg-white p-6 shadow-lg dark:bg-gray-900">
	<!-- Header with Title and Status -->
	<div class="flex flex-col items-center justify-between border-b pb-4 md:flex-row">
		<h2 class="text-2xl font-bold text-gray-900 dark:text-white">
			{name}
		</h2>
		<div class="mt-4 flex items-center space-x-4 md:mt-0">
			<!-- Status Badge -->
			<span
				class="rounded-full px-3 py-1 text-sm font-medium
        {isPublic ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}"
			>
				{isPublic ? 'Public' : 'Private'}
			</span>
			<!-- Join Button -->
			<button
				class="rounded bg-blue-600 px-4 py-2 font-semibold text-white transition hover:bg-blue-700"
			>
				Join Community +
			</button>
		</div>
	</div>

	<!-- Description -->
	<p class="text-gray-700 dark:text-gray-300">
		{description}
	</p>

	<!-- Tags -->
	{#if tags && tags.length > 0}
		<div class="flex flex-wrap gap-2">
			{#each tags as tag}
				<span
					class="rounded-full bg-gray-200 px-3 py-1 text-sm text-gray-700 dark:bg-gray-800 dark:text-gray-200"
				>
					{tag}
				</span>
			{/each}
		</div>
	{/if}

	<!-- Degrees -->
	{#if degrees && degrees.length > 0}
		<div class="flex flex-wrap gap-2">
			{#each degrees as degree}
				<span
					class="rounded-full bg-gray-200 px-3 py-1 text-sm text-gray-700 dark:bg-gray-800 dark:text-gray-200"
				>
					{degree}
				</span>
			{/each}
		</div>
	{/if}

	<!-- Bottom Row: Total Members & Creation Date -->
	<div class="flex items-center justify-between border-t pt-4 text-gray-600 dark:text-gray-400">
		<div class="flex items-center space-x-2">
			<span class="text-lg font-bold text-gray-900 dark:text-white">{totalMembers}</span>
			<span class="text-sm">Members</span>
		</div>
		<div class="text-sm">
			{creationDate}
		</div>
	</div>
</div>

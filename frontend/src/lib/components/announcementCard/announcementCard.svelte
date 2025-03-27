<script lang="ts">
	export let title: string = 'Announcement Title';
	export let description: string = 'Announcement Description';

	export let datetime: string = '2025-01-01';

	export let tags: string[] = [];
</script>

<div class="w-full max-w-2xl rounded-lg bg-gray-100 p-4 shadow-md dark:bg-gray-800">
	<!-- Title Section -->
	<div class="mb-2 flex items-center justify-between">
		<h1 class="text-xl font-bold text-gray-900 dark:text-white">
			{title}
		</h1>
	</div>

	<!-- Location, Date and Duration Section -->
	<div class="mb-2 flex items-center justify-between">
		<p class="text-lg font-semibold text-gray-900 dark:text-white">
			{datetime}
		</p>
	</div>

	<!-- Description -->
	<p class="text-sm text-gray-700 dark:text-gray-300">
		{description}
	</p>

	<!-- Tags -->
	<div class="mt-3 flex flex-wrap gap-2">
		{#each tags as tag}
			<span class="rounded bg-gray-300 px-2 py-1 text-sm dark:bg-gray-600">
				{tag}
			</span>
		{/each}
	</div>
</div>

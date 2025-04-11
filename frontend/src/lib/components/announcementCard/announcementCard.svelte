
<script lang="ts">
	export let title: string = 'Announcement Title';
	export let description: string = 'Announcement Description';
	export let datetime: string = '2025-01-01';
	export let tags: string[] = [];
</script>

<div class="mx-auto my-3 flex w-full max-w-[500px] flex-col justify-between rounded-2xl bg-white p-3 shadow-xl sm:m-2 sm:p-5">
	<!-- Title Section -->
	<div class="flex items-center justify-between">
		<h1 class="text-xl font-bold text-gray-800">
			{title}
		</h1>
	</div>

	<!-- Description -->
	<p class="text-sm text-gray-600 my-2">
		{description}
	</p>

	<!-- Tags -->
	<!-- Tags Section -->
{#if tags.length > 0}
<div class="flex flex-wrap gap-2 my-2">
	{#each tags as tag}
		<span
			class="rounded-lg bg-gray-200 px-3 py-1.5 text-sm font-medium text-black
					shadow-sm border border-gray-300 hover:shadow-md transition-shadow
					duration-200 transform hover:-translate-y-0.5"
		>
			{"#" + tag}
		</span>
	{/each}
</div>
{/if}


	<!-- Date Section -->
	<div class="mt-2 flex items-center justify-between text-gray-500 text-sm">
		<p>
			{datetime}
		</p>
	</div>
</div>
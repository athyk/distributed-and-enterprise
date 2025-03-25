<script lang="ts">
	export let postedName: string = 'Alex';
	export let communityHeader: string = 'Tech Innovators';
	export let community: string = 'Software Development';

	export let description: string =
		'Join a vibrant community of developers, designers, and tech enthusiasts. Collaborate on projects, share insights, and drive innovation in the tech industry.';
	export let tags: string[] = ['JavaScript', 'Svelte', 'React', 'Tailwind', 'Node.js'];

	export let creationDate: string = 'February 2021';
</script>

<div class="w-full max-w-2xl rounded-lg bg-gray-100 p-4 shadow-md dark:bg-gray-800">
	<div class="mb-2 flex items-center justify-between">
		<h1 class="text-xl font-bold text-gray-900 dark:text-white">
			{communityHeader}
		</h1>
	</div>

	<div class="mb-2 flex items-center justify-between">
		<h2 class="text-lg font-semibold text-gray-900 dark:text-white">
			Posted By: {postedName}
		</h2>
		<h2 class="text-lg font-semibold text-gray-900 dark:text-white">
			Community: {community}
		</h2>
	</div>

	<p class="text-sm text-gray-700 dark:text-gray-300">{description}</p>

	<div class="mt-3 flex items-center justify-between">
		<div class="flex flex-wrap gap-2">
			{#each tags as tag}
				<span class="rounded bg-gray-300 px-2 py-1 text-sm dark:bg-gray-600">
					{tag}
				</span>
			{/each}
		</div>
		<p class="text-sm text-gray-500 dark:text-gray-400">{creationDate}</p>
	</div>
</div>

<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { goto } from '$app/navigation'; // Import goto for navigation

	export let communitiesInfo: { id: number; name: string; imageUrl: string }[];

	const dispatch = createEventDispatcher();

	function selectCommunity(id: number) {
		dispatch('selectCommunity', id);
	}

	function createCommunity() {
		goto('communities/create'); // Redirects to /create page
	}
</script>

<ul class="h-full space-y-2 bg-gray-800 p-4 text-white">
	{#each communitiesInfo as community}
		<li class="flex items-center space-x-3 rounded p-2 hover:bg-gray-600">
			<button
				on:click={() => selectCommunity(community.id)}
				class="flex w-full items-center space-x-3 text-left"
			>
				<img src={community.imageUrl} alt={community.name} class="h-10 w-10 rounded-full" />
				<span>{community.name}</span>
			</button>
		</li>
	{/each}

	<!-- Create Community Button -->
	<button
		on:click={createCommunity}
		class="mt-4 w-full rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-600"
	>
		+ Create Community
	</button>
</ul>

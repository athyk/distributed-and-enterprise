<script lang="ts">
	import { goto } from '$app/navigation';

	// Define properties for the profile section.
	export let userInfo: {
		id: number;
		name: string;
		imageUrl?: string;
		isOnline?: boolean;
	}[];

	// Sort users by online status (online users first)
	$: sortedUserInfo = [...userInfo].sort((a, b) => (b.isOnline ? 1 : 0) - (a.isOnline ? 1 : 0));

	function goToSettings() {
		goto('/settings'); // Update the path as needed
	}
</script>

<aside class="flex h-screen w-full max-w-xs flex-col bg-white p-6 shadow-lg dark:bg-gray-800">
	<!-- Users List (Scrollable) -->
	<div class="flex-1 space-y-4 overflow-y-auto">
		{#each sortedUserInfo as user (user.id)}
			<div class="relative flex items-center rounded-md bg-gray-100 p-2 dark:bg-gray-700">
				<div class="relative">
					<img
						src={user.imageUrl || 'https://via.placeholder.com/40'}
						alt={user.name}
						class="h-10 w-10 rounded-full object-cover"
					/>
					{#if user.isOnline}
						<span
							class="absolute right-0 bottom-0 block h-3 w-3 rounded-full border-2 border-white bg-green-500 dark:border-gray-800"
						></span>
					{:else}
						<span
							class="absolute right-0 bottom-0 block h-3 w-3 rounded-full border-2 border-white bg-gray-500 dark:border-gray-800"
						></span>
					{/if}
				</div>
				<span class="ml-3 text-sm font-medium text-gray-900 dark:text-gray-100">
					{user.name}
				</span>
			</div>
		{/each}
	</div>

	<!-- Settings Button -->
	<button
		on:click={goToSettings}
		class="mt-4 w-full rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-600"
	>
		⚙️ Settings
	</button>
</aside>

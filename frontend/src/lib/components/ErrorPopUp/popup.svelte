<script lang="ts">
	export let errorMessage = '';
	import { onMount } from 'svelte';

	let timeoutId: ReturnType<typeof setTimeout>;

	$: if (errorMessage) {
		if (timeoutId) clearTimeout(timeoutId);
		timeoutId = setTimeout(() => {
			errorMessage = '';
		}, 5000);
	}

	onMount(() => {
		return () => {
			if (timeoutId) clearTimeout(timeoutId);
		};
	});
</script>

{#if errorMessage}
	<div
		class="fixed inset-0 z-[9999] flex items-start justify-center pt-4 sm:items-start sm:justify-end sm:pr-4"
	>
		<div class="mb-4 w-full max-w-md rounded bg-red-500 p-4 text-white shadow-xl">
			<p>{errorMessage}</p>
			<button
				class="mt-2 rounded bg-white px-2 py-1 text-red-500"
				on:click={() => (errorMessage = '')}>Close</button
			>
		</div>
	</div>
{/if}

<script lang="ts">
	export let errorMessage = '';
	export let positive = false;

	let colour = 'bg-red-500';

	$:if (positive) {
		colour = 'bg-green-500';
	}else {
		colour = 'bg-red-500';
	}
</script>

{#if errorMessage}
	<div class="absolute top-0 right-0 w-full p-4 sm:w-1/4">
		<div class="mb-4 w-full rounded bg-red-500 p-4 text-white shadow-lg">
			<p>{errorMessage}</p>
			<button
				class="mt-2 rounded bg-white px-2 py-1 text-red-500"
				on:click={() => (errorMessage = '')}>Close</button
			>
		</div>
	</div>
{/if}

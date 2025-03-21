<script lang="ts">
	export let errorMessage = '';
</script>

{#if errorMessage}
	<div class="absolute top-0 right-0 w-1/2 p-4">
		<div class="mb-4 w-full rounded bg-red-500 p-4 text-white shadow-lg">
			<p>{errorMessage}</p>
			<button
				class="mt-2 rounded bg-white px-2 py-1 text-red-500"
				on:click={() => (errorMessage = '')}>Close</button
			>
		</div>
	</div>
{/if}

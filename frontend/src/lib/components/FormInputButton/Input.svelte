<script lang="ts">
	export let value = '';
	export let type = 'text';
	export let Name = '';
	export let placeholder = '';
	export let showLabel = false;
</script>

<div class="mt-4">
	{#if showLabel}
		<label for={Name} class="block text-gray-700">{Name} </label>
	{/if}

	<input
		{type}
		id={Name}
		name={Name}
		{placeholder}
		bind:value
		class="mt-2 w-full rounded-md border px-4 py-2 focus:ring-1 focus:ring-blue-600 focus:outline-none"
		required
	/>
</div>

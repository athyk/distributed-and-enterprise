<script lang="ts">
	export let type: 'submit' | 'button' | 'reset' = 'submit';
	export let disabled = false;
	export let onClick = () => {};
	export let text = 'Submit';
</script>

<button
	{type}
	{disabled}
	on:click={onClick}
	class="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-900"
>
	{text}
</button>

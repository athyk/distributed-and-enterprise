<script lang="ts">
	import { get } from '$lib/api/get';
	import { onMount } from 'svelte';

	async function getUser() {
		let response = await get('users/@me');
		console.log(response);
	}

	onMount(() => {
		getUser();
	});
</script>

<div style="text-align: center;">
	<h1>Welcome to UniHub</h1>
</div>

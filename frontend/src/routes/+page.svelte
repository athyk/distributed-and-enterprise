<script lang="ts">
	import Input from '$lib/components/FormInputButton/Input.svelte';

	let email = '';

	$: console.log(email);
</script>

<h1>Welcome to UniHub</h1>

<Input
	Name="Email"
	placeholder="Enter your email"
	type="email"
	showLabel={true}
	bind:value={email}
/>

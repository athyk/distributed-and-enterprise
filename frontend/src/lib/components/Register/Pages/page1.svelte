<script lang="ts">
	import Input from '$components/FormInput/Input.svelte';
	export let email = '';
	export let password = '';
	export let passwordConfirm = '';
	export let pageInputs: Input[] = [];
</script>

<Input
	Name="Email"
	placeholder="Enter your email"
	type="email"
	showLabel={true}
	required={true}
	bind:value={email}
	bind:this={pageInputs[0]}
/>
<Input
	Name="Password"
	placeholder="Enter your password"
	type="password"
	showLabel={true}
	required={true}
	bind:value={password}
	bind:this={pageInputs[1]}
/>
<Input
	Name="Confirm Password"
	placeholder="Confirm your password"
	type="password"
	showLabel={true}
	required={true}
	bind:value={passwordConfirm}
	bind:this={pageInputs[2]}
/>

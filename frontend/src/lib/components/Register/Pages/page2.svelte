<script lang="ts">
	import Input from '$components/FormInput/Input.svelte';

	export let fName = '';
	export let lName = '';
	export let dob = '';
	export let gender = '';

	export let pageInputs: Input[] = [];
</script>

<Input
	Name="First Name"
	placeholder="Enter your first name"
	type="text"
	showLabel={true}
	required={true}
	bind:value={fName}
	bind:this={pageInputs[0]}
/>
<Input
	Name="Last Name"
	placeholder="Enter your last name"
	type="text"
	showLabel={true}
	required={true}
	bind:value={lName}
	bind:this={pageInputs[1]}
/>
<Input
	Name="Date of Birth"
	placeholder="Enter your date of birth"
	type="date"
	showLabel={true}
	required={true}
	bind:value={dob}
	bind:this={pageInputs[2]}
/>
<Input
	Name="Gender"
	placeholder="Enter your Gender"
	type="text"
	showLabel={true}
	required={true}
	bind:value={gender}
	bind:this={pageInputs[3]}
/>

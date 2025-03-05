<script lang="ts">
	import Input from '$components/FormInput/Input.svelte';

	export let degree = '';
	export let degreeYear = '';
	export let graduationYear = '';
	export let tags = '';

	export let pageInputs: Input[] = [];
</script>

<Input
	Name="Degree"
	placeholder="Enter your degree"
	type="text"
	showLabel={true}
	required={true}
	bind:value={degree}
	bind:this={pageInputs[0]}
/>
<Input
	Name="Current Year of Study"
	placeholder="1"
	type="number"
	showLabel={true}
	bind:value={degreeYear}
	required={true}
	minValue={1}
	maxValue={5}
	bind:this={pageInputs[1]}
/>
<Input
	Name="Graduation Year"
	placeholder="2025"
	type="number"
	showLabel={true}
	bind:value={graduationYear}
	required={true}
	minValue={2025}
	maxValue={2030}
	bind:this={pageInputs[2]}
/>
<!-- <Input
	Name="Tags"
	placeholder="Enter your tags"
	type="text"
	required={true}
	showLabel={true}
	bind:value={tags}
	bind:this={pageInputs[3]}
/> -->

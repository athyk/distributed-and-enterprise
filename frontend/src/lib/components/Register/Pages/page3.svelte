<script lang="ts">
	import Input from '$components/FormInput/Input.svelte';
	import SearchBox from '$components/SearchBox/searchBox.svelte';
	import { get } from '$lib/api/get';
	import type { response } from '$lib/api/types';

	export let degree: string[] = [];
	export let degreeYear = '';
	export let graduationYear = '';
	export let tags: string[] = [];

	export let pageInputs: Input[] = [];

	async function getDegrees(){
		let response = await get('degrees') as response;
		if(response.http_status === 200){
			return response.data;
		}
	}

	async function getTags(){
		let response = await get('tags') as response;
		if(response.http_status === 200){
			return response.data;
		}
	}

</script>

<SearchBox
	data={getDegrees()}
	maxItems={1}
	showLabel={true}
	Name="Degree"
	placeholder="Select your Degree"
	bind:chosenItems={degree}
	bind:this={pageInputs[0]}
/>

<Input
	Name="Current Year of Study"
	placeholder="1"
	type="number"
	showLabel={true}
	required={true}
	minValue={1}
	maxValue={5}
	bind:value={degreeYear}
	bind:this={pageInputs[1]}
/>

<Input
	Name="Graduation Year"
	placeholder="2025"
	type="number"
	showLabel={true}
	required={true}
	minValue={2025}
	maxValue={2030}
	bind:value={graduationYear}
	bind:this={pageInputs[2]}
/>

<SearchBox
	data={getTags()}
	maxItems={5}
	showLabel={true}
	Name="Tags"
	placeholder="Enter your tags"
	bind:this={pageInputs[3]}
	bind:chosenItems={tags}
/>

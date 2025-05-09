<script lang="ts">
	import CreateEditBase from '$components/Post/CreateEdit/base.svelte';
	import CreateDescription from '$components/Post/Sections/Inputs/createDescription.svelte';
	import SearchBox from '$components/SearchBox/searchBox.svelte';
	import type { response, communityData } from '$lib/api/apiType';
	import Popup from '$components/ErrorPopUp/popup.svelte';
	import { onMount } from 'svelte';
	import { getTagID } from '$lib/api/getTagID';
	import { getDegreeID } from '$lib/api/getDegreeID';
	import { get } from '$lib/api/get';
	import { Put } from '$lib/api/Put';
	import { checkPermisions } from '$lib/api/checkUser';

	let formData = {
		name: '',
		description: '',
		public: false,
		tags: [] as [string, number][],
		degrees: [] as [string, number][]
	};

	let error_message = '';
	export let communityID: number;
	export let modalShown = false;
	export let refreshCommunity = 0;
	let hasPermission = false;

	async function editCommunity() {
		if (!hasPermission) {
			console.error('User does not have permission to edit this community.');
			return;
		}
		error_message = '';
		console.log('Creating community with data:', formData);
		const formattedData = {
			...formData,
			tags: formData.tags.map((tag) => tag[1]),
			degrees: formData.degrees.map((degree) => degree[1])
		};
		console.log('Formatted data:', formattedData);
		try {
			let response = (await Put('community/' + communityID, formattedData)) as response;
			if (response.success === true) {
				modalShown = false;
				refreshCommunity += 1;
			} else {
				error_message = response.error_message[0];
			}
		} catch (error) {
			console.error('Error creating community:', error);
			error_message = 'Error creating community. Please try again.';
		}
	}

	function Submit2() {
		editCommunity();
	}

	function hideModal() {
		modalShown = false;
		console.log('Hiding modal');
	}

	async function getTags(response: communityData) {
		if (response.tags && response.tags.length > 0) {
			response.tags.forEach(async (tagName) => {
				const TagID = await getTagID(tagName.toString());
				formData.tags.push([tagName, TagID]);
			});
		}
	}

	async function getDegree(response: communityData) {
		if (response.degrees && response.degrees.length > 0) {
			response.degrees.forEach(async (degreeName) => {
				const TagID = await getDegreeID(degreeName.toString());
				formData.degrees.push([degreeName, TagID]);
			});
		}
	}

	async function getCommunity() {
		console.log('Fetching community data...');
		if (await checkPermisions(communityID)) {
			console.log('User has permissions to edit the community.');
			hasPermission = true;
		} else {
			console.error('User does not have permissions to edit the community.');
			hasPermission = false;
			hideModal();
			return;
		}
		try {
			const response = (await get('community/' + communityID)) as communityData;
			formData.name = response.name;
			formData.description = response.description;
			formData.public = response.public_community;
			getTags(response);
			getDegree(response);
		} catch (error) {
			console.error('Error fetching community data:', error);
		}
	}

	onMount(() => {
		hasPermission = false;
		console.log('Community ID:', communityID);
		formData.tags = [];
		formData.degrees = [];
		if (communityID) {
			getCommunity();
		} else {
			console.error('Community ID is not provided or invalid.');
		}
	});
</script>

{#if modalShown}
	<div
		class="bg-gray bg-opacity-75 fixed inset-0 z-60 flex items-center justify-center p-4 backdrop-blur-sm"
	>
		<Popup bind:errorMessage={error_message} />
		<!-- Container -->
		<CreateEditBase
			ModalTitle={'Edit Community'}
			onSubmit={Submit2}
			onClose={hideModal}
			ButtonText={'Edit'}
		>
			<svelte:fragment slot="content">
				<div class="flex w-full flex-col">
					<label for="Community_Name" class="mb-1 text-sm font-semibold">Community Name</label>
					<input
						id="Community_Name"
						placeholder="Community Name"
						bind:value={formData.name}
						class="w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
					/>
				</div>
				<div class="flex w-full flex-col">
					<label for="Community_Description" class="mt-1 text-sm font-semibold"
						>Community Description</label
					>
					<CreateDescription bind:text={formData.description} />
				</div>
				<div class="flex w-full flex-col">
					<label for="Community_Public" class="mt-1 text-sm font-semibold">Community Tags</label>
					<SearchBox
						classStyle="w-full border-2 border-gray-300 rounded-lg p-2 mt-2 focus:outline-none focus:border-blue-500"
						marginTop=""
						placeholder="Search for Tags..."
						url="tags/list/"
						id="tags"
						multi_select={true}
						max_select={5}
						bind:selected={formData.tags}
					/>
				</div>
				<div class="flex w-full flex-col">
					<label for="Community_Public" class="mt-1 text-sm font-semibold">Community Degrees</label>
					<SearchBox
						classStyle="w-full border-2 border-gray-300 rounded-lg p-2 mt-2 focus:outline-none focus:border-blue-500"
						marginTop=""
						placeholder="Search for Degrees..."
						url="degrees/list/"
						id="degrees"
						multi_select={true}
						max_select={5}
						bind:selected={formData.degrees}
					/>
				</div>
				<div class="mt-2 flex items-center">
					<input
						type="checkbox"
						id="Community_Public"
						bind:checked={formData.public}
						class="mr-2"
					/>
					<label for="Community_Public" class="text-sm font-semibold">Public Community</label>
				</div></svelte:fragment
			>
		</CreateEditBase>
	</div>
{/if}

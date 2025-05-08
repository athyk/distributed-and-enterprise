<script lang="ts">
	import { post } from '$lib/api/post';
	import CreateEditBase from '$components/Post/CreateEdit/base.svelte';
	import CreateDescription from '$components/Post/Sections/Inputs/createDescription.svelte';
	import SearchBox from '$components/SearchBox/searchBox.svelte';
	import type { response } from '$lib/api/apiType';
	import Popup from '$components/ErrorPopUp/popup.svelte';

	let formData = {
		name: '',
		description: '',
		public: false,
		tags: [] as [string, number][],
		degrees: [] as [string, number][]
	};

	let error_message = '';
	export let modalShown = false;

	async function createCommunity() {
		error_message = '';
		console.log('Creating community with data:', formData);
		const formattedData = {
			...formData,
			tags: formData.tags.map((tag) => tag[1]),
			degrees: formData.degrees.map((degree) => degree[1])
		};
		console.log('Formatted data:', formattedData);
		try {
			let response = (await post('community/', formattedData)) as response;
			if (response.id != -1) {
				window.location.href = `/communities/${response.id}`;
			} else {
				error_message = response.error_message[0];
			}
		} catch (error) {
			console.error('Error creating community:', error);
			error_message = 'Error creating community. Please try again.';
		}
	}

	function Submit() {
		createCommunity();
	}

	function hideModal() {
		modalShown = false;
		console.log('Hiding modal');
	}
</script>

{#if modalShown}
	<div
		class="bg-gray bg-opacity-75 fixed inset-0 z-50 flex items-center justify-center p-4 backdrop-blur-sm"
	>
		<Popup bind:errorMessage={error_message} />
		<!-- Container -->
		<CreateEditBase
			ModalTitle={'Create Community'}
			onSubmit={Submit}
			onClose={hideModal}
			ButtonText={'Create'}
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

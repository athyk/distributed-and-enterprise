<script lang="ts">
	import { onMount } from 'svelte';

	import CreateEditBase from './base.svelte';
	import CreateTitle from '../Sections/Inputs/createTitle.svelte';
	import CreateDescription from '../Sections/Inputs/createDescription.svelte';
	import SearchBox from '$components/SearchBox/searchBox.svelte';

	import { post } from '$lib/api/post';
	import { Put } from '$lib/api/Put';
	import { getSingleAnnouncement } from '$lib/api/singleItem/annoucement';
	import type { response } from '$lib/api/apiType';

	export let showModal = false;
	export let onClose = () => {};
	export let onSuccess = () => {};
	export let edit: boolean = false;
	export let editID: number = 0;
	export let communityID: number = 1;

	let modalTitle = '';
	let submitText = '';

	let title = '';
	let text = '';
	let tags: [string, number][] = [];

	async function submitAnnoucement() {
		let data = {
			title: title,
			description: text,
			tags: tags.map((tag) => tag[1])
		};
		let response = {} as response;
		if (edit) {
			response = (await Put(
				'community/' + communityID + '/announcements/' + editID,
				data
			)) as response;
		} else {
			response = (await post('community/' + communityID + '/announcements', data)) as response;
		}

		if (response.success === true) {
			console.log('Annoucement Action Done');
			title = '';
			text = '';
			onSuccess();
			onClose();
			showModal = false;
		} else {
			console.error('Error creating post:', response.error_message);
		}
	}

	function getPost() {
		if (editID === 0) return;
		getSingleAnnouncement(communityID, editID)
			.then((response) => {
				if (response) {
					title = response.title;
					text = response.description;
					tags = (response.tags as [string, number][]).map((tag) => [tag[0], tag[1]]);
				} else {
					console.error('Error: response is undefined');
				}
			})
			.catch((error) => {
				console.error('Error fetching post:', error);
			});
	}

	onMount(() => {
		modalTitle = edit ? 'Edit Annoucement' : 'Create an Annoucement';
		submitText = edit ? 'Edit Annoucement' : 'Annouce';
		if (edit) {
			getPost();
		}
	});
</script>

<CreateEditBase
	ModalTitle={modalTitle}
	{showModal}
	{onClose}
	onSubmit={submitAnnoucement}
	ButtonText={submitText}
>
	<svelte:fragment slot="content">
		<CreateTitle bind:title />
		<CreateDescription bind:text />
		<SearchBox
			classStyle="w-full border-2 border-gray-300 rounded-lg p-2 mt-2 focus:outline-none focus:border-blue-500"
			marginTop=""
			placeholder="Search for Tags..."
			url="tags/list/"
			id="tags"
			multi_select={true}
			max_select={5}
			bind:selected={tags}
		/>
	</svelte:fragment>
</CreateEditBase>

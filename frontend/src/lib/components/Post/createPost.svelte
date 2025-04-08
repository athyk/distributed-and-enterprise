<script lang="ts">
	import type {
		postCreateResponse,
		singlePostResponse,
		PaginationDataResponse,
		response,
		singleAnnoucementResponse
	} from '$lib/api/apiType';
	import { post } from '$lib/api/post';
	import { get } from '$lib/api/get';
	import { Put } from '$lib/api/Put';

	import { isLoggedIn } from '$lib/api/checkUser';

	import Base from './base.svelte';
	import CreateTitle from './Sections/Inputs/createTitle.svelte';
	import CreateDescription from './Sections/Inputs/createDescription.svelte';
	import Title from './Sections/title.svelte';
	import ImageInput from './Sections/Inputs/imageInput.svelte';
	import SearchBox from '$components/SearchBox/searchBox.svelte';
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';


	let title = '';
	let text = '';
	let images = [] as string[];
	let tags: [string, number][] = [];

	export let showModal = false;
	export let success = false;
	export let edit = false;
	export let editID: number | undefined = undefined;
	export let feedType: 'posts' | 'events' | 'announcements' = 'posts';
	export let communityID = 1 as number;

	export let onClose = () => {};
	export let onSuccess = () => {};

	let ModalTitle = 'Create a Post';
	let ButtonText = 'Post';

	async function onSubmit() {
		if ((await checkUserPermission()) === false) {
			return;
		}
		switch (feedType) {
			case 'posts':
				if (edit){
					await editPost();
				} else {
					await createPost();
				}
				break;
			case 'events':
				break;
			case 'announcements':
				if (edit) {
					await editAnnoucement();
				} else {
					await createAnnoucement();
				}
			default:
				break;
		}
		onSuccess();
		onClose();
	}

	async function createPost() {
		let data = {
			title: title,
			description: text,
			images: images,
			tags: tags.map((tag) => tag[1])
		};
		let response = (await post('posts/', data)) as postCreateResponse;
		if (response.success === true) {
			console.log('Post created successfully');
			title = '';
			text = '';
			images = [];
			success = true;
			showModal = false;
		} else {
			console.error('Error creating post:', response.error_message);
		}
	}

	async function createAnnoucement() {
		let data = {
			title: title,
			description: text,
			tags: tags.map((tag) => tag[1])
		};
		let response = (await post('community/' + communityID + '/announcements', data)) as response;
		if (response.success === true) {
			console.log('Announcement created successfully');
			title = '';
			text = '';
			images = [];
			success = true;
			showModal = false;
		} else {
			console.error('Error creating announcement:', response.error_message);
		}
	}

	async function editAnnoucement() {
		let data = {
			title: title,
			description: text,
			tags: tags.map((tag) => tag[1])
		};
		let response = (await Put(
			'community/' + communityID + '/announcements/' + editID,
			data
		)) as response;
		if (response.success === true) {
			console.log('Announcement edited successfully');
			title = '';
			text = '';
			images = [];
			success = true;
			showModal = false;
		} else {
			console.error('Error editing announcement:', response.error_message);
		}
	}

	async function editPost() {
		let data = {
			post_id: editID,
			title: title,
			description: text,
			tags: tags.map((tag) => tag[1]),
			images: images
		};
		let response = (await Put('posts/', data)) as postCreateResponse;
		if (response.success === true) {
			console.log('Post edited successfully');
			title = '';
			text = '';
			images = [];
			success = true;
			showModal = false;
		} else {
			console.error('Error editing post:', response.error_message);
		}
	}

	function closeModal() {
		showModal = false;
	}

	function handleKeydown(event: KeyboardEvent) {
		if (showModal) {
			if (event.key === 'Escape') {
				closeModal();
			}
		}
	}

	async function checkUserPermission() {
		if ((await isLoggedIn()) === false) {
			console.log('User is not logged in');
			showModal = false;
			return false;
		}
		console.log('User is logged in');
		return true;
	}

	async function getTagID(name: string) {
		let response = (await get('tags/list/?name=' + name)) as PaginationDataResponse;
		if (response.success === true) {
			console.log('Tag ID fetched successfully');
			return response.tags[0].id;
		} else {
			console.error('Error fetching tag ID:', response.error_message);
			return -1;
		}
	}

	async function getPostData() {
		if (edit) {
			let response = (await get('posts/?post_id=' + editID)) as singlePostResponse;
			if (response.success === true) {
				console.log('Post data fetched successfully');
				title = response.post.title;
				text = response.post.description;
				images = response.post.images;
				let newTags: [string, number][] = [];
				for (let i = 0; i < response.post.tags.length; i++) {
					newTags.push([response.post.tags[i], await getTagID(response.post.tags[i])]);
				}
				tags = newTags;
				console.log('Tags:', tags);
			} else {
				console.error('Error fetching post data:', response.error_message);
			}
		}
	}

	async function getAnnoucementData() {
		if (edit) {
			let response = (await get(
				'community/' + communityID + '/announcements/' + editID
			)) as singleAnnoucementResponse;
			if (response.success === true) {
				console.log('Announcement data fetched successfully');
				title = response.announcement.title;
				text = response.announcement.description;
				let newTags: [string, number][] = [];
				for (let i = 0; i < response.announcement.tags.length; i++) {
					newTags.push([
						response.announcement.tags[i],
						await getTagID(response.announcement.tags[i])
					]);
				}
				tags = newTags;
				console.log('Tags:', tags);
			} else {
				console.error('Error fetching announcement data:', response.error_message);
			}
		}
	}

	function handleEditView() {
		switch (feedType) {
			case 'posts':
				ModalTitle = 'Create a Post';
				ButtonText = 'Post';
				if (edit) {
					ModalTitle = 'Edit Post';
					ButtonText = 'Update Post';
					getPostData();
				}
				break;
			case 'events':
				ModalTitle = 'Create an Event';
				ButtonText = 'Event';
				break;
			case 'announcements':
				ModalTitle = 'Create an Announcement';
				ButtonText = 'Announce';
				if (edit) {
					ModalTitle = 'Edit Announcement';
					ButtonText = 'Update Announcement';
					getAnnoucementData();
				}
				break;
			default:
				break;
		}
	}

	onMount(() => {
		if (browser) {
			window.addEventListener('keydown', handleKeydown);
		}
		checkUserPermission();
		handleEditView();
	});

	onDestroy(() => {
		if (browser) {
			window.removeEventListener('keydown', handleKeydown);
		}
	});
</script>

<Base>
	<Title>{ModalTitle}</Title>
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
	></SearchBox>
	{#if feedType === 'posts'}
		<ImageInput bind:images />
	{/if}
	{#if feedType === 'events'}
		<SearchBox
			classStyle="w-full border-2 border-gray-300 rounded-lg p-2 mt-2 focus:outline-none focus:border-blue-500"
			marginTop=""
			placeholder="Search for location..."
			url=""
			id="location"
			multi_select={false}
			max_select={1}
		></SearchBox>
		<input type="datetime-local" class="mt-2 w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none" />
	{/if}
	<div
		class="mt-2 flex w-full items-center justify-between rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
	>
		<button
			class="rounded bg-green-500 px-4 py-2 text-white"
			on:click|preventDefault|stopPropagation={onSubmit}
		>
			{ButtonText}
		</button>
		{#if feedType === 'posts'}
			<button
				class="rounded bg-yellow-500 px-4 py-2 text-white"
				on:click={() => document.getElementById('fileInput')?.click()}
			>
				Upload Image
			</button>
		{/if}
		<button class="rounded bg-red-500 px-4 py-2 text-white" on:click={closeModal}> Close </button>
	</div>
</Base>

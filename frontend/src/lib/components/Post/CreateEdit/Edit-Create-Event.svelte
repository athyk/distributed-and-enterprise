<script lang="ts">
	import { onMount } from 'svelte';

	import CreateEditBase from './base.svelte';
	import CreateTitle from '../Sections/Inputs/createTitle.svelte';
	import CreateDescription from '../Sections/Inputs/createDescription.svelte';
	import SearchBox from '$components/SearchBox/searchBox.svelte';
	import Popup from '$components/ErrorPopUp/popup.svelte';

	import type { response } from '$lib/api/apiType';

	import { post } from '$lib/api/post';
	import { Put } from '$lib/api/Put';
	import { getEventData } from '$lib/api/singleItem/event';

	export let showModal = false;
	export let onClose = () => {};
	export let onSuccess = () => {};
	export let edit: boolean = false;
	export let editID: number = 0;
	export let communityID: number = 1;

	let modalTitle = '';
	let submitText = '';
	const today = new Date().toISOString().slice(0, 16);

	let title = '';
	let text = '';
	let location: [string, string, string][] = [];
	let datetime_value = '';
	let duration_value = 1;
	let tags: [string, number][] = [];
	let error_message = '';

	async function submitEvent() {
		const formattedDatetime = new Date(datetime_value).toISOString().split('T')[0];
		let data = {
			title: title,
			description: text,
			location: location[0][2],
			datetime: formattedDatetime,
			duration: duration_value,
			tags: tags.map((tag) => tag[1]),
			lat_lng: [parseFloat(location[0][0]), parseFloat(location[0][1])]
		};
		let response = {} as response;
		if (edit) {
			console.log('Edit event:', editID);
			console.log(data);
			response = (await Put('community/' + communityID + '/events/' + editID, data)) as response;
		} else {
			response = (await post('community/' + communityID + '/events', data)) as response;
		}
		if (response.success === true) {
			console.log('Event created successfully');
			title = '';
			text = '';
			showModal = false;
			onSuccess();
			onClose();
		} else {
			error_message = response.error_message[0];
			console.error('Error creating event:', response.error_message);
		}
	}

	async function getEvent() {
		if (editID === 0) return;
		getEventData(communityID, editID).then((response) => {
			if (response) {
				title = response.title;
				text = response.description;
				if (response.latitude && response.longitude) {
					location = [
						[response.latitude.toString(), response.longitude.toString(), response.location]
					];
				} else {
					location = [['', '', response.location]];
				}
				datetime_value = new Date(response.datetime).toISOString().slice(0, 16);
				duration_value = parseInt(response.duration, 10);
				tags = (response.tags as [string, number][]).map((tag) => [tag[0], tag[1]]);
			} else {
				console.error('Error fetching event data');
			}
		});
	}

	onMount(() => {
		title = '';
		text = '';
		location = [['', '', '']];
		datetime_value = '';
		duration_value = 1;
		tags = [];
		error_message = '';
		modalTitle = edit ? 'Edit Event' : 'Create an Event';
		submitText = edit ? 'Edit Event' : 'Create Event';
		if (edit) {
			getEvent();
		}
	});

	$: if (showModal) {
		console.log('Modal shown', showModal, edit);
		title = '';
		text = '';
		location = [['', '', '']];
		datetime_value = '';
		duration_value = 1;
		tags = [];
		error_message = '';
		modalTitle = edit ? 'Edit Event' : 'Create an Event';
		submitText = edit ? 'Edit Event' : 'Create Event';
		if (edit) {
			getEvent();
		}
	}

</script>


<Popup bind:errorMessage={error_message} />
<CreateEditBase
	ModalTitle={modalTitle}
	{showModal}
	{onClose}
	onSubmit={submitEvent}
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
		<SearchBox
			classStyle="w-full border-2 border-gray-300 rounded-lg p-2 mt-2 focus:outline-none focus:border-blue-500"
			marginTop=""
			placeholder="Search for location..."
			url=""
			id="location"
			multi_select={false}
			max_select={1}
			location={true}
			bind:location_selected={location}
		></SearchBox>
		<input
			type="datetime-local"
			min={today}
			class="mt-2 w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
			bind:value={datetime_value}
		/>
		<input
			type="number"
			min="1"
			class="mt-2 w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
			placeholder="Duration"
			bind:value={duration_value}
		/>
	</svelte:fragment>
</CreateEditBase>

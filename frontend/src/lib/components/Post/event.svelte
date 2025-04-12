<script lang="ts">
	import Post from './base.svelte';
	import Title from './Sections/title.svelte';
	import Text from './Sections/text.svelte';
	import Tags from './Sections/tags.svelte';
	import Map from './Sections/Map/map.svelte';
	import Time from './Sections/time.svelte';
	import Popup from '$components/ErrorPopUp/popup.svelte';

	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';

	import { get } from '$lib/api/get';
	import type { EventDataResponse, EventResponse, response } from '$lib/api/apiType';
	import { deleteCall } from '$lib/api/delete';

	let data: EventDataResponse[] = [];
	export let url = '';
	export let offset = 0;
	export let limit = 10;
	export let fixed = false;
	export let params = '';
	let end = false;
	let formatted_url = '';
	let errorMessage = '';

	async function GetPosts() {
		formatted_url = url + '?offset=' + offset + '&limit=' + limit+"&"+params;
		const response = (await get(formatted_url)) as EventResponse;
		if (response.success === true) {
			const globalEvents = response.global_events || [];
			const events = response.events || [];
			let chosenEvents = [];

			if (globalEvents.length === 0) {
				chosenEvents = events;
			} else {
				chosenEvents = globalEvents;
			}

			if (chosenEvents.length === 0) {
				console.log('No posts found');
				end = true;
			} else if (events.length < limit) {
				end = true;
			}

			if (data.length > 0) {
				data = [...data, ...chosenEvents];
			} else {
				data = chosenEvents;
			}
			console.log('Posts fetched successfully:', data);
		} else {
			console.error('Error fetching posts:', response.error_message);
			return [];
		}
	}

	async function handleDelete(event: CustomEvent) {
		const postId = event.detail.id;
		console.log('Deleting post with ID:', postId);
		const response = (await deleteCall(
			'community/' + event.detail.communityId + '/events/' + postId,
			{}
		)) as response;
		if (response.success === true) {
			console.log('Event deleted successfully');
			data = data.filter((post) => post.id !== postId);
			errorMessage = 'Event deleted successfully';
			GetPosts();
		} else {
			console.error('Error deleting Event:', response.error_message);
		}
	}

	function handleBottomSroll() {
		console.log('Bottom scroll reached');
		if (end || fixed) {
			console.log('No more posts to load');
			return;
		}
		offset += limit;
		GetPosts();
	}

	type DeletePostEvent = CustomEvent<{ id: number; communityId?: number }>;
	const deleteEventHandler = (e: Event) => handleDelete(e as DeletePostEvent);

	onMount(() => {
		GetPosts();
		if (browser) {
			document.addEventListener('deletePost', deleteEventHandler);
			document.addEventListener('scrollbottomreach', handleBottomSroll);
		}
	});

	onDestroy(() => {
		if (browser) {
			document.removeEventListener('deletePost', deleteEventHandler);
			document.removeEventListener('scrollbottomreach', handleBottomSroll);
		}
	});
</script>

<Popup bind:errorMessage />
{#each data as event, index (event.id + '-' + index)}
	<Post id={event.id} communityID={event.community_id}>
		<Title slot="header">
			{event.title}
			{#if event.location}
				at {event.location}
			{/if}
		</Title>
		<Time datetime={event.datetime} duration={event.duration} />
		<Tags tags={event.tags} />

		<Text>
			{event.description}
		</Text>
		<Map lat={event.latitude} lon={event.longitude} />
	</Post>
{/each}

<script lang="ts">
	import Post from './base.svelte';
	import Title from './Sections/title.svelte';
	import Text from './Sections/text.svelte';
	import Tags from './Sections/tags.svelte';
	import Map from './Sections/Map/map.svelte';
	import Time from './Sections/time.svelte';

	import { onMount,onDestroy } from 'svelte';
	import { browser } from '$app/environment';

	import { get } from '$lib/api/get';
	import type { EventDataResponse, EventResponse } from '$lib/api/apiType';

	let data: EventDataResponse[] = [];
	export let url = '';
	export let offset = 0;
	export let limit = 10;
	export let fixed = false;
	let end = false;
	let formatted_url = '';


	async function GetPosts() {
		formatted_url = url + '?offset=' + offset + '&limit=' + limit;
		const response = (await get(formatted_url)) as EventResponse;
		if (response.success === true) {
			if (response.global_events.length === 0) {
				console.log('No posts found');
				end = true;
			} else if (response.global_events.length < limit) {
				end = true;
			}

			if (data.length > 0) {
				data = [...data, ...response.global_events];
			} else {
				data = response.global_events;
			}
		} else {
			console.error('Error fetching posts:', response.error_message);
			return [];
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

	onMount(() => {
		GetPosts();
		if (browser) {
			document.addEventListener('scrollbottomreach', handleBottomSroll);
		}
	});

	onDestroy(() => {
		if (browser) {
			document.removeEventListener('scrollbottomreach', handleBottomSroll);
		}
	});

</script>

{#each data as event, index (event.id + '-' + index)}
	<Post id={event.id}>
		<Title>{event.title}</Title>
		<Time datetime={event.datetime} />
		<Tags tags={event.tags} />

		<Text>
			{event.description}
		</Text>
		<!-- <Map lat={event.latitude} lon={event.longitude} /> -->
		<Map lat={51.501793} lon={-2.548713} />
	</Post>
{/each}
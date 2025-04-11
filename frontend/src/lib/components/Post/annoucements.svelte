<script lang="ts">
	import Post from './base.svelte';
	import type { globalAnnouncementData, globalAnnouncement, response } from '$lib/api/apiType.ts';
	import { get } from '$lib/api/get';
	import { deleteCall } from '$lib/api/delete';
	import Title from './Sections/title.svelte';
	import Text from './Sections/text.svelte';
	import Tags from './Sections/tags.svelte';
	import { browser } from '$app/environment';
	import Popup from '$components/ErrorPopUp/popup.svelte';

	import { onMount, onDestroy } from 'svelte';

	export let url = '';
	export let offset = 0;
	export let limit = 10;
	export let fixed = false;
	let end = false;
	let formatted_url = '';
	let errorMessage = '';

	let data: globalAnnouncementData[] = [];

	function converTimetoUnix(date: string) {
		const dateObj = new Date(date);
		const unixTime = Math.floor(dateObj.getTime() / 1000);
		return unixTime.toString();
	}

	async function GetAnnouncments() {
		formatted_url = url + '?offset=' + offset + '&limit=' + limit;
		const response = (await get(formatted_url)) as globalAnnouncement;
		if (response.http_status === 200) {
			if (response.global_announcements.length === 0) {
				console.log('No announcements found');
				end = true;
			} else if (response.global_announcements.length < limit) {
				end = true;
			}

			if (data.length > 0) {
				data = [...data, ...response.global_announcements];
			} else {
				data = response.global_announcements;
			}
		} else {
			console.error('Error fetching announcements:', response.error_message);
			return [];
		}
	}

	async function handleDelete(event: CustomEvent) {
		const postId = event.detail.id;
		const communityId = event.detail.communityId;
		console.log('Deleting post with ID:', postId);
		let url = 'community/' + communityId + '/announcements/' + postId;
		const response = (await deleteCall(url, {})) as response;
		if (response.success === true) {
			console.log('Post deleted successfully');
			data = data.filter((post) => post.id !== postId);
			errorMessage = 'Post deleted successfully';
			GetAnnouncments();
		} else {
			console.error('Error deleting post:', response.error_message);
			errorMessage = response.error_message[0];
		}
	}

	function handleBottomSroll() {
		console.log('Bottom scroll reached');
		if (end || fixed) {
			console.log('No more posts to load');
			return;
		}
		offset += limit;
		GetAnnouncments();
	}

	onMount(() => {
		GetAnnouncments();
		if (browser) {
			document.addEventListener('deletePost', (e: Event) =>
				handleDelete(e as CustomEvent<{ id: number; communityId: number }>)
			);
			document.addEventListener('scrollbottomreach', handleBottomSroll);
		}
	});

	onDestroy(() => {
		if (browser) {
			document.removeEventListener('deletePost', (e: Event) =>
				handleDelete(e as CustomEvent<{ id: number; communityId: number }>)
			);
			document.removeEventListener('scrollbottomreach', handleBottomSroll);
		}
	});
</script>

<Popup bind:errorMessage />

{#each data as announcement, index (announcement.id + '-' + index)}
	<Post
		author={announcement.user}
		date={converTimetoUnix(announcement.uploaded)}
		id={announcement.id}
		communityID={announcement.community_id}
	>
		<Title>{announcement.title}</Title>
		<Tags tags={announcement.tags} />
		<Text>{announcement.description}</Text>
	</Post>
{/each}

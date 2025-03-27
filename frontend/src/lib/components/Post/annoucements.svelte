<script lang="ts">
	import Post from './base.svelte';
	import type { globalAnnouncementData, globalAnnouncement, response } from '$lib/api/apiType.ts';
	import { get } from '$lib/api/get';
	import { deleteCall } from '$lib/api/delete';
	import Title from './Sections/title.svelte';
	import Text from './Sections/text.svelte';
	import Tags from './Sections/tags.svelte';
	import { browser } from '$app/environment';

	import { onMount, onDestroy } from 'svelte';

	export let url = '';

	let data: globalAnnouncementData[] = [];

	function converTimetoUnix(date: string) {
		const dateObj = new Date(date);
		const unixTime = Math.floor(dateObj.getTime() / 1000);
		return unixTime.toString();
	}

	async function GetAnnouncments() {
		const response = (await get(url)) as globalAnnouncement;
		if (response.http_status === 200) {
			data = response.global_announcements;
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
			alert('Annoucement deleted successfully');
			GetAnnouncments();
		} else {
			console.error('Error deleting post:', response.error_message);
		}
	}

	onMount(() => {
		GetAnnouncments();
		if (browser) {
			document.addEventListener('deletePost', (e: Event) =>
				handleDelete(e as CustomEvent<{ id: number; communityId: number }>)
			);
		}
	});

	onDestroy(() => {
		if (browser) {
			document.removeEventListener('deletePost', (e: Event) =>
				handleDelete(e as CustomEvent<{ id: number; communityId: number }>)
			);
		}
	});
</script>

{#each data as announcement (announcement.id)}
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

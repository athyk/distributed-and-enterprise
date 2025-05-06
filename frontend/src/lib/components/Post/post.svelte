<script lang="ts">
	import Post from './base.svelte';
	import Title from './Sections/title.svelte';
	import Text from './Sections/text.svelte';
	import Tags from './Sections/tags.svelte';
	import Gallery from './Sections/gallery.svelte';
	import Popup from '$components/ErrorPopUp/popup.svelte';

	import type { postsData, postResponse, response } from '$lib/api/apiType';
	import { get } from '$lib/api/get';
	import { deleteCall } from '$lib/api/delete';
	import { browser } from '$app/environment';

	import { onMount, onDestroy } from 'svelte';

	let data: postsData[] = [];
	let errorMessage = '';
	export let url = '';
	export let offset = 0;
	export let limit = 10;
	export let fixed = false;
	export let params = 1;
	let formatted_url = '';
	let end = false;

	async function GetPosts() {
		formatted_url = url + '?offset=' + offset + '&limit=' + limit+"&"+params;
		const response = (await get(formatted_url)) as postResponse;
		if (response.success === true) {
			if (response.posts.length === 0) {
				console.log('No posts found');
				end = true;
			} else if (response.posts.length < limit) {
				end = true;
			}

			if (data.length > 0) {
				data = [...data, ...response.posts];
			} else {
				data = response.posts;
			}
		} else {
			console.error('Error fetching posts:', response.error_message);
			return [];
		}
	}

	async function handleDelete(event: CustomEvent) {
		const postId = event.detail.id;
		console.log('Deleting post with ID:', postId);
		const response = (await deleteCall('posts/', { id: postId })) as response;
		if (response.success === true) {
			console.log('Post deleted successfully');
			data = data.filter((post) => post.id !== postId);
			errorMessage = 'Post deleted successfully';
			GetPosts();
		} else {
			console.error('Error deleting post:', response.error_message);
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
{#each data as post, index (post.id + '-' + index)}
	<Post author={post.user_data} date={post.created_at} id={post.id}>
		{#if post.title}
			<Title>{post.title}</Title>
		{/if}
		{#if post.tags.length > 0}
			<Tags tags={post.tags} />
		{/if}

		{#if post.description}
			<Text>
				{post.description}
			</Text>
		{/if}

		{#if post.images.length > 0}
			<Gallery images={post.images} />
		{/if}
	</Post>
{/each}

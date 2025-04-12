<script lang="ts">
	import type { UserInfo } from '$lib/api/apiType';
	import { isUserID } from '$lib/api/checkUser';
	import { onMount } from 'svelte';
	export let author: UserInfo = {} as UserInfo;
	export let id = 0 as number;
	let ownPost = false as boolean;
	let url = '';

	async function isAuthor() {
		return await isUserID(author.user_id, true);
	}

	onMount(() => {
		isAuthor().then((result) => {
			ownPost = result;
		});
		if (!author.user_id) {
			console.warn('No User ID is not defined');
			return;
		}
		url = '/user/' + author.user_id.toString();
	});
</script>

<div
	class="top-0 flex items-center space-x-2 rounded-t-2xl bg-white"
	id={'header-' + id.toString()}
>
	{#if author.picture_url}
		<a href={url} target="_blank" rel="noopener noreferrer">
			<img src={author.picture_url} alt="Profile Icon" class="h-11 w-11 rounded-full" />
		</a>
	{:else if url != ''}
		<a href={url} target="_blank" rel="noopener noreferrer">
			<img
				src="https://picsum.photos/id/63/200/200"
				alt="Profile Icon"
				class="h-11 w-11 rounded-full"
			/>
		</a>
	{/if}
	<span class="font-bold">{author.first_name} {author.last_name}</span>
	{#if ownPost && author.user_id}
		<span class="text-sm text-gray-500">(You)</span>
	{/if}
</div>

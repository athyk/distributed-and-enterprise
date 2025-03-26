<script lang="ts">
	import Annoucements from '$components/Post/annoucements.svelte';
	import Feed from '$components/Post/feed.svelte';
	import Post from '$components/Post/post.svelte';
	import Event from '$lib/components/Post/event.svelte';

	let choice = 0;
</script>

<div class="mt-4 flex items-center justify-center">
	<input
		type="button"
		class="rounded bg-blue-500 px-4 py-2 text-white"
		value="Posts "
		on:click={() => (choice = 0)}
	/>
	<input
		type="button"
		class="m-2 rounded bg-blue-500 px-4 py-2 text-white"
		value="Events"
		on:click={() => (choice = 1)}
	/>
	<input
		type="button"
		class="rounded bg-blue-500 px-4 py-2 text-white"
		value="Annoucements"
		on:click={() => (choice = 2)}
	/>
</div>

<div class="flex min-h-screen items-center justify-center">
	{#if choice === 0}
		<Feed feedType="posts">
			<Post url="posts/list?offset=0&limit=10" slot="Posts" />
		</Feed>
	{:else if choice === 1}
		<Feed feedType="events">
			<Event url="community/events?offset=0&limit=10" slot="Posts" />
		</Feed>
	{:else if choice === 2}
		<Feed feedType="announcements">
			<Annoucements url="community/announcements?offset=0&limit=10" slot="Posts" />
		</Feed>
	{/if}
</div>

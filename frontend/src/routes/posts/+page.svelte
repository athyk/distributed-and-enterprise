<script lang="ts">
	import Feed from '$components/Post/feed.svelte';
	import Annoucements from '$components/Post/annoucements.svelte';
	import Post from '$components/Post/post.svelte';
	import Event from '$lib/components/Post/event.svelte';

	let choice = 0;
</script>

<h1 class="pt-5 text-center text-3xl font-bold">Testing</h1>
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
		value="Events Community 1"
		on:click={() => (choice = 1)}
	/>
	<input
		type="button"
		class="rounded bg-blue-500 px-4 py-2 text-white"
		value="Annoucements"
		on:click={() => (choice = 2)}
	/>
</div>

<div class="flex min-h-screen items-center justify-center px-4">
	{#if choice === 0}
		<div class="w-full max-w-4xl">
			<Feed feedType="posts">
				<Post url="posts/list" slot="Posts" limit={30} />
			</Feed>
		</div>
	{:else if choice === 1}
		<div class="w-full max-w-4xl">
			<Feed feedType="events" showActions={true} communityID={1}>
				<Event url="community/1/events" slot="Posts" limit={30} />
			</Feed>
		</div>
	{:else if choice === 2}
		<div class="w-full max-w-4xl">
			<Feed feedType="announcements">
				<Annoucements url="community/announcements" slot="Posts" limit={30} />
			</Feed>
		</div>
	{/if}
</div>

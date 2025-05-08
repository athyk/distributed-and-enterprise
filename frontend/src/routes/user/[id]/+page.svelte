<script lang="ts">
	import Feed from '$components/Post/feed.svelte';
	import Post from '$components/Post/post.svelte';
	import Userheader from '$components/Post/UserInfo/userheader.svelte';
	import { page } from '$app/stores';
	let user_id = parseInt($page.params.id);
	let refreshKey = 0;
</script>

<div class="flex min-h-screen flex-col px-4">
	<div class="mx-auto w-full max-w-4xl">
		<Userheader bind:user_id bind:refreshKey />

		{#if user_id}
			<Feed feedType="posts" showActions={true} {refreshKey}>
				<Post url="posts/list" slot="Posts" params="user_id={user_id}" offset={0} />
			</Feed>
		{:else}
			<p class="text-center text-gray-500">Loading user information...</p>
		{/if}
	</div>
</div>

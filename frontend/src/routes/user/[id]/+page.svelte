<script lang="ts">
    import Feed from '$components/Post/feed.svelte';
    import Post from '$components/Post/post.svelte';
    import Userheader from '$components/Post/UserInfo/userheader.svelte';
    import { page } from '$app/stores';
    let user_id = parseInt($page.params.id);
    let refreshKey = 0;

</script>

<div class="flex min-h-screen px-4 flex-col">
    <div class="w-full max-w-4xl mx-auto">
		<Userheader bind:user_id={user_id} bind:refreshKey={refreshKey} />

        {#if user_id}
            <Feed feedType="posts" showActions={true} refreshKey={refreshKey}>
                <Post url="posts/list" slot="Posts" params="user_id={user_id}" offset={0} />
            </Feed>
        {:else}
            <p class="text-center text-gray-500">Loading user information...</p>
        {/if}
    </div>
</div>

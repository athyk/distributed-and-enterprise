<script lang="ts">
	import Feed from '$components/Post/feed.svelte';
	import Post from '$components/Post/post.svelte';
	import Userheader from '$components/Post/UserInfo/userheader.svelte';
	let user_id = 1;

</script>

<div class="flex min-h-screen px-4 flex-col">
    <div class="w-full max-w-4xl mx-auto">
		<Userheader user_id={user_id} />

        <Feed feedType="posts" showActions={true}>
            <Post url="posts/list" slot="Posts" params="user_id={user_id}" offset={0} />
        </Feed>
    </div>
</div>

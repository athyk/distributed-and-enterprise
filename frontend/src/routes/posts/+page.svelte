<script lang="ts">
	import Annoucements from "$components/Post/annoucements.svelte";
    import Feed from "$components/Post/feed.svelte";
	import Post from "$components/Post/post.svelte";
    import Event from "$lib/components/Post/event.svelte";


    let choice = 0;


</script>

<div class="flex justify-center items-center mt-4">
    <input type="button" class="bg-blue-500 text-white px-4 py-2 rounded" value="Posts " on:click={() => choice = 0} />
    <input type="button" class="bg-blue-500 text-white px-4 py-2 rounded m-2 " value="Events" on:click={() => choice = 1} />
    <input type="button" class="bg-blue-500 text-white px-4 py-2 rounded" value="Annoucements" on:click={() => choice = 2} />
</div>


<div class="flex justify-center items-center min-h-screen">
    {#if choice === 0}
        <Feed feedType="posts">
            <Post url="posts/list?offset=0&limit=10" slot="Posts"/>
        </Feed>
    {:else if choice === 1}
        <Feed feedType="events">
            <Event url="community/events?offset=0&limit=10" slot="Posts"/>
        </Feed>
    {:else if choice === 2}
        <Feed feedType="announcements">
            <Annoucements url="community/announcements?offset=0&limit=10" slot="Posts"/>
        </Feed>
    {/if}
</div>

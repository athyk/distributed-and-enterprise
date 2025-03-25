<script lang="ts">
    import Post from "./base.svelte";
    import Title from "./Sections/title.svelte";
    import Text from "./Sections/text.svelte";
    import Tags from "./Sections/tags.svelte";
    import Gallery from "./Sections/gallery.svelte";

    import type { postsData,postResponse } from "$lib/api/apiType";
    import { get } from "$lib/api/get";

    import { onMount } from "svelte";


    let data: postsData[] = []
    export let url = '';

    async function GetPosts(){
        const response = await get(url) as postResponse
        if (response.success === true) {
            data = response.posts;
            console.log(data);
        } else {
            console.error("Error fetching posts:", response.error_message);
            return [];
        }
    }

    onMount(() => {
        GetPosts();
    });

</script>

{#each data as post (post.id)}
    <Post
        author={post.user_data}
        date={post.created_at}
        id={post.id}
        ownPost={false}
    >
        {#if post.title}
            <Title>{post.title}</Title>
        {/if}

        {#if post.tags}
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



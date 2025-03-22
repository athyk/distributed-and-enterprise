<script lang="ts">
    import Post from "./base.svelte";

    import Title from "./Sections/title.svelte";
    import Text from "./Sections/text.svelte";
    import Tags from "./Sections/tags.svelte";
    import Gallery from "./Sections/gallery.svelte";

    import type { postsData } from "$lib/api/apiType";


    export let data: postsData[] = []

</script>

{#each data as post (post.id)}
    <Post
        author={{
            name: "I need an API",
            profile_image: "https://picsum.photos/id/433/300/300",
            URL: "/",
        }}
        date={post.created_at}
        id={post.id}
        likes={0}
        showLikes={true}
        ownPost={false}
    >
        {#if post.title}
            <Title>{post.title}</Title>
        {/if}

        <!-- {#if post.tags}
            <Tags tags={post.tags} />
        {/if} -->

        {#if post.description}
            <Text>{post.description}</Text>
        {/if}

        <!-- {#if post.images}
            <Gallery images={post.images} />
        {/if} -->
    </Post>
{/each}
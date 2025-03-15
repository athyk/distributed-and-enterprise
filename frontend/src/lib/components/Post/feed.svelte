<script lang="ts">
    import Create from "$components/Post/create.svelte";
    import Gallery from "$components/Post/Sections/gallery.svelte";
    import Post from "$components/Post/post.svelte";
    import Text from "$components/Post/Sections/text.svelte";
	import Title from "$components/Post/Sections/title.svelte";
    import Tags from "$components/Post/Sections/tags.svelte";
    import Event from "$components/Post/Sections/event.svelte";

    import Masonry from 'svelte-bricks';
    import { onMount } from "svelte";

    export let data = [] as {
        author: {
            name: string,
            profile_image: string,
            URL: string,
            DegreeYear?: string,
            Degree?: string,
        },
        title?: string,
        datetime: string,
        images?: string[],
        likes: number,
        tags?: string[],
        id: number,
        text?: string,
        event?: {
            title: string,
            description: string,
            start_time: string,
            end_time: string,
            location: {
                name: string,
                lat: number,
                lon: number,
            },
        },
    }[];

    data = [...data,...data];

    let items = Array.from({ length: data.length }, (_, i) => i);



    export let minColWidth = 300;
    export let maxColWidth = 600;
    export let gap = 16;
    export let width = 1080;
    export let height = 1920;

    onMount(() => {
        width = window.innerWidth;
        window.addEventListener("resize", () => {
            width = window.innerWidth;
        });
    });


</script>




<div class="w-full flex flex-wrap justify-center">
    <Create />
    <Masonry
        items={items}
        minColWidth={minColWidth}
        maxColWidth={maxColWidth}
        gap={gap}
        masonryWidth={width}
        masonryHeight={height}
    >
        {#snippet children({ item })}
            <div class="w-full max-w-sm">
                <Post
                    author={data[item].author}
                    date={data[item].datetime}
                    likes={data[item].likes}
                    id={data[item].id}
                    ownPost={true}
                >
                    {#if data[item].title}
                        <Title>{data[item].title}</Title>
                    {/if}
                    {#if (data[item].tags ?? []).length >= 1}
                        <Tags tags={data[item].tags} />
                    {/if}
                    {#if (data[item].images ?? []).length >= 1}
                        <Gallery
                            images_urls={data[item].images}
                        />
                    {/if}
                    {#if data[item].event}
                        <Event event={data[item].event} />
                    {/if}
                    {#if data[item].text}
                        <Text>{data[item].text}</Text>
                    {/if}
                </Post>
            </div>
        {/snippet}
    </Masonry>
</div>
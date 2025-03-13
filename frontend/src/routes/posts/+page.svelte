<script lang="ts">
    import Gallery from "$components/Post/gallery.svelte";
import Post from "$components/Post/post.svelte";
    import Text from "$components/Post/text.svelte";

    const temp_data = [
        {
            author: "John Doe",
            datetime: "1741894310",
            text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.",
            likes: 0,
            id: 1,
        },
        {
            author: "Jane Smith",
            datetime: "1741894311",
            text: "Another example of a post with some dummy text. This is just to show how multiple posts can be rendered on the page.",
            likes: 5,
            id: 2,
        },
        {
            author : "Jake Stuckey",
            datetime: "1741894312",
            text: "This is the third post in the list. It is a bit shorter than the previous ones, but it still serves the purpose of showing how the posts are rendered.",
            likes: 2,
            id: 3,
        },
    ];


</script>

<div class="flex flex-col items-center p-5">
    <div class="w-full max-w-lg overflow-hidden">
        {#each temp_data as post}
            <Post
                author={post.author}
                date={post.datetime}
                likes={post.likes}
                id={post.id}
                ownPost={true}
            >
            <Gallery
                images_urls={["https://picsum.photos/seed/a/1920/1080", "https://picsum.photos/seed/b/1920/1080", "https://picsum.photos/1920/1080"]}
            />
            <Text>{post.text}</Text>

            </Post>
        {/each}
    </div>
</div>

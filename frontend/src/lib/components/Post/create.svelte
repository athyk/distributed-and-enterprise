<script lang="ts">
    import SearchBox from "$components/SearchBox/searchBox.svelte";
    let title = '';
    let text = '';
    let images = [] as string[];
    let event = {
        title: '',
        description: '',
        start_time: '',
        end_time: '',
        location: {
            name: '',
            lat: 0,
            lon: 0,
        },
    };

    function onSubmit() {
        alert('title = ' + title + '\ntext = ' + text);
    }

</script>

<div class="w-full max-w-2xl p-4">
    <form>
        <div class="w-full flex flex-col items-center p-4">
            <h1 class="text-2xl font-bold mb-2">Create Post</h1>
            <textarea
                class="w-full max-w-2xl h-15 p-2 border rounded-t resize-none"
                placeholder="Enter your title here..."
                bind:value={title}
            ></textarea>
            <textarea
                class="w-full max-w-2xl h-32 p-2 border-l border-r resize-none"
                placeholder="Enter your post here..."
                bind:value={text}
            ></textarea>
            <textarea
                class="w-full max-w-2xl h-15 p-2 border-l border-r border-t resize-none"
                placeholder="Search for Tags..."
            ></textarea>
            <div class="w-full max-w-2xl h-15 p-5 border rounded-b flex items-center justify-between">
                <button class="bg-blue-500 text-white px-4 py-2 rounded" on:click={onSubmit}>
                    Post
                </button>
                <button class="bg-blue-500 text-white px-4 py-2 rounded">Add Image</button>
                <button class="bg-blue-500 text-white px-4 py-2 rounded">Add Event</button>
            </div>
        </div>
    </form>
</div>

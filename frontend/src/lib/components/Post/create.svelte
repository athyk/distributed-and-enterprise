<script lang="ts">
    import SearchBox from "$components/SearchBox/searchBox.svelte";
    import type { postCreateResponse,ImageUploadResponse } from "$lib/api/apiType";
    import { post } from "$lib/api/post";
    let title = '';
    let text = '';
    let images = [] as string[];

    export let success = false;

    async function onSubmit() {
        let data = {
            title: title,
            description: text,
            images: images,
            tags: [],
        }
        let response = await post("posts/", data) as postCreateResponse;
        if (response.success === true) {
            console.log("Post created successfully");
            title = '';
            text = '';
            images = [];
            success = true;
        } else {
            console.error("Error creating post:", response.error_message);
        }
    }

    async function fileSelected(event: Event) {
        if (!event.target || !(event.target as HTMLInputElement).files) {
            console.error("No file selected");
            return;
        }

        const file = (event.target as HTMLInputElement).files?.[0];
        if (!file) {
            console.error("No file selected");
            return;
        }
        const formData = new FormData();
        formData.append("file", file);

        try {
            let imageResponse = await post("posts/upload", {}, formData) as ImageUploadResponse;
            if (imageResponse.success === true) {
                console.log("Image uploaded successfully");
                images = [...images, imageResponse.file_url];
                console.log(images);
            } else {
                console.error("Error uploading image:", imageResponse.error);
            }
        } catch (error) {
            console.error("Error uploading image:", error);
        }
    }

    $: console.log("Images:", images);

</script>


<div class="flex flex-col justify-between min-h-[50px] bg-white rounded-2xl border-black border-2 p-5">
    <form>
        <div class="w-full flex flex-col items-center p-4">
            <h1 class="text-2xl font-bold mb-2">Create Post</h1>
            <textarea
                class="w-full max-w-2xl h-15 p-2 border rounded-t resize-none"
                placeholder="Enter your title here..."
                bind:value={title}
            ></textarea>
            <SearchBox
                classStyle="w-[10000px] max-w-2xl h-16 p-2 border-l border-r border-b resize-none"
                marginTop=""
                placeholder="Search for Tags..."
                url="tags/list"
                id="tags"
                multi_select={true}
                max_select={5}
            ></SearchBox>
            <textarea
                class="w-full max-w-2xl h-32 p-2 border-l border-r "
                placeholder="Enter your post here..."
                bind:value={text}
            ></textarea>

            {#if images.length > 0}
                <div class="w-full max-w-2xl p-2 border-l border-r border-b">
                    <h1 class="text-lg font-bold mb-2">Images ({images.length})</h1>
                    <!-- Horizontal scrollable container -->
                    <div class="flex flex-row gap-2 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-100">
                        {#each images as image, i (i)}
                            <div class="flex-shrink-0">
                                <img 
                                    src={image}
                                    alt="User uploaded"
                                    class="h-[100px] w-auto object-cover rounded"
                                />
                                <!-- Optional: Add a remove button -->
                                <button 
                                    class="mt-1 text-xs text-red-500 hover:text-red-700"
                                    on:click={() => images = images.filter((_, index) => index !== i)}
                                >
                                    Remove
                                </button>
                            </div>
                        {/each}
                    </div>
                </div>
            {/if}
            <div class="w-full max-w-2xl h-15 p-5 border rounded-b flex items-center justify-between">
                <button class="bg-blue-500 text-white px-4 py-2 rounded" on:click={onSubmit}>
                    Post
                </button>
                <input
                    type="file"
                    accept="image/*"
                    id="fileInput"
                    class="hidden"
                    on:change={fileSelected}
                />
                <button class="bg-blue-500 text-white px-4 py-2 rounded" on:click={() => document.getElementById('fileInput')?.click()}>
                    Upload Image
                </button>
        </div>
    </form>
</div>

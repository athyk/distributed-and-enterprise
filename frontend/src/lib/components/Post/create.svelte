<script lang="ts">
    import SearchBox from "$components/SearchBox/searchBox.svelte";
    import type { postCreateResponse,ImageUploadResponse } from "$lib/api/apiType";
    import { post } from "$lib/api/post";

    import Base from "./base.svelte";
	import CreateTitle from "./Sections/Inputs/createTitle.svelte";
    import CreateDescription from "./Sections/Inputs/createDescription.svelte";
    import Title from "./Sections/title.svelte";

    let title = '';
    let text = '';
    let images = [] as string[];

    export let showModal = false;

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
            showModal = false;
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

    function closeModal() {
        showModal = false;
    }

</script>

<Base>
    <Title>Create A Post</Title>
    <CreateTitle bind:title />
    <CreateDescription bind:text />
    <SearchBox
        classStyle="w-full border-2 border-gray-300 rounded-lg p-2 mt-2 focus:outline-none focus:border-blue-500"
        marginTop=""
        placeholder="Search for Tags..."
        url="tags/list"
        id="tags"
        multi_select={true}
        max_select={5}
    ></SearchBox>
    {#if images.length > 0}
        <div class="w-full border-2 border-gray-300 rounded-lg p-2 mt-2 focus:outline-none focus:border-blue-500">
            <h1 class="text-lg font-bold mb-2">Images ({images.length})</h1>
            <div class="flex flex-row gap-2 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-100">
                {#each images as image, i (i)}
                    <div class="flex-shrink-0">
                        <img 
                            src={image}
                            alt="User uploaded"
                            class="h-[100px] w-auto object-cover rounded"
                        />
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
    <div class="w-full border-2 border-gray-300 rounded-lg p-2 mt-2 focus:outline-none focus:border-blue-500 items-center justify-between flex">
        <button class="bg-green-500 text-white px-4 py-2 rounded" on:click|preventDefault|stopPropagation={onSubmit}> Post </button>
        <input
            type="file"
            accept="image/*"
            id="fileInput"
            class="hidden"
            on:change={fileSelected}
        />
        <button class="bg-yellow-500 text-white px-4 py-2 rounded" on:click={() => document.getElementById('fileInput')?.click()}> Upload Image </button>
        <button class="bg-red-500 text-white px-4 py-2 rounded" on:click={closeModal}> Close </button>
    </div>

</Base>
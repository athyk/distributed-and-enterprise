<script lang="ts">
    import { browser } from '$app/environment';
    import { onMount } from 'svelte';

    import  CreateEditBase from './base.svelte';
    import CreateTitle from '../Sections/Inputs/createTitle.svelte';
	import CreateDescription from '../Sections/Inputs/createDescription.svelte';
    import ImageInput from '../Sections/Inputs/imageInput.svelte';
	import SearchBox from '$components/SearchBox/searchBox.svelte';

    import { post } from '$lib/api/post';
	import { Put } from '$lib/api/Put';
    import { getPostData } from '$lib/api/singleItem/post';
    import type { postCreateResponse,postsData } from '$lib/api/apiType';

    export let showModal = false;
    export let onClose = () => {};
	export let onSuccess = () => {};
    export let edit: boolean = false;
    export let editID: number = 0;

    let modalTitle = '';
    let submitText = '';

    let title = '';
    let text = '';
    let images = [] as string[];
	let tags: [string, number][] = [];
    let success = false;


    async function submitPost() {
        let data: { title: string; description: string; images: string[]; tags: number[]; post_id?: number } = {
            title: title,
            description: text,
            images: images,
            tags: tags.map((tag) => tag[1])
        };
        let response = {} as postCreateResponse;
        if (edit) {
            data = {
                ...data,
                "post_id": editID
            };
            response = (await Put('posts/', data)) as postCreateResponse;
        }else {
            response = (await post('posts/', data)) as postCreateResponse;
        }

		if (response.success === true) {
			console.log('Post Action Done');
			title = '';
			text = '';
			images = [];
			success = true;
			onSuccess();
            onClose();
            showModal = false;
		} else {
			console.error('Error creating post:', response.error_message);
		}
	}

    function uploadImage() {
        if (browser) {
            document.getElementById('fileInput')?.click();
        }
    }

    function getPost(){
        if (editID === 0) return;
        getPostData(editID).then((response: postsData | undefined) => {
            if (response) {
                title = response.title;
                text = response.description;
                images = response.images;
                tags = (response.tags as [string, number][]).map((tag) => [tag[0], tag[1]]);
            } else {
                console.error('Error: response is undefined');
            }
        });
    }

    onMount(() => {
        modalTitle = edit ? 'Edit Post' : 'Create Post';
        submitText = edit ? 'Edit Post' : 'Create Post';
        if (edit) {
            getPost();
        }
    });

</script>


<CreateEditBase
    ModalTitle={modalTitle}
    showModal={showModal}
    onClose={onClose}
    onSubmit={submitPost}
    ButtonText={submitText}
>

    <svelte:fragment slot="content">
        <CreateTitle bind:title />
        <CreateDescription bind:text />
        <SearchBox
            classStyle="w-full border-2 border-gray-300 rounded-lg p-2 mt-2 focus:outline-none focus:border-blue-500"
            marginTop=""
            placeholder="Search for Tags..."
            url="tags/list/"
            id="tags"
            multi_select={true}
            max_select={5}
            bind:selected={tags}
        />
        <ImageInput bind:images />
    </svelte:fragment>

    <svelte:fragment slot="actions">
        <button
        class="rounded bg-yellow-500 px-4 py-2 text-white"
        on:click={() => uploadImage()}
        >
            Upload Image
        </button>
    </svelte:fragment>

</CreateEditBase>
<script lang="ts">
	import { post } from '$lib/api/post';
	import type { ImageUploadResponse } from '$lib/api/apiType';
	export let images = [] as string[];
	export let inputID = 'fileInput';

	export async function fileSelected(event: Event) {
		if (!event.target || !(event.target as HTMLInputElement).files) {
			console.error('No file selected');
			return;
		}

		const file = (event.target as HTMLInputElement).files?.[0];
		if (!file) {
			console.error('No file selected');
			return;
		}
		const formData = new FormData();
		formData.append('file', file);

		try {
			let imageResponse = (await post('posts/upload', {}, formData)) as ImageUploadResponse;
			if (imageResponse.success === true) {
				console.log('Image uploaded successfully');
				images = [...images, imageResponse.file_url];
				console.log(images);
			} else {
				console.error('Error uploading image:', imageResponse.error);
			}
		} catch (error) {
			console.error('Error uploading image:', error);
		}
	}
</script>

<input type="file" accept="image/*" id={inputID} class="hidden" on:change={fileSelected} />

<div
	class="mt-2 min-h-[200px] w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
>
	<h1 class="mb-2 text-lg font-bold">Images ({images.length})</h1>
	<div
		class="scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-100 flex flex-row gap-2 overflow-x-auto pb-2"
	>
		{#each images as image, i (i)}
			<div class="flex-shrink-0">
				<img src={image} alt="User uploaded" class="h-[100px] w-auto rounded object-cover" />
				<button
					class="mt-1 text-xs text-red-500 hover:text-red-700"
					on:click={() => (images = images.filter((_, index) => index !== i))}
				>
					Remove
				</button>
			</div>
		{/each}
	</div>
</div>

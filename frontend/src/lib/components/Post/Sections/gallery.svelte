<script lang="ts">
	import { onMount } from 'svelte';
	export let images: string[] = [];

	let image: number = 0;
	let showModal = false;

	function removeInvalidImages() {
		images = images.filter((image) => {
			const img = new Image();
			img.src = image;
			return img.complete;
		});
	}

	function nextImage() {
		image = (image + 1) % images.length;
	}

	function prevImage() {
		image = (image - 1 + images.length) % images.length;
	}

	function openModal(event: MouseEvent) {
		console.log('openModal', image);
		const clickedImage = event.currentTarget as HTMLElement;
		if (clickedImage && clickedImage.id) {
			image = parseInt(clickedImage.id, 10);
		}
		showModal = true;
	}

	function closeModal() {
		showModal = false;
	}

	function handleKeydown(event: KeyboardEvent) {
		if (showModal) {
			if (event.key === 'ArrowRight') {
				nextImage();
			} else if (event.key === 'ArrowLeft') {
				prevImage();
			} else if (event.key === 'Escape') {
				closeModal();
			}
		}
	}

	window.addEventListener('keydown', handleKeydown);

	onMount(() => {
		removeInvalidImages();
	});
</script>

{#if images.length > 0}
	<div class="relative flex flex-col items-center overflow-hidden">
		<div class="w-full max-w-2xl p-2">
			<div
				class="scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-100 flex flex-row gap-2 overflow-x-auto pb-2"
			>
				{#each images as image, i (i)}
					<div class="flex-shrink-0" on:click={openModal} aria-hidden="true" id={i.toString()}>
						<img
							src={image}
							alt="User uploaded"
							class="h-[100px] w-auto rounded object-cover transition duration-200 hover:cursor-pointer hover:opacity-75 hover:shadow-lg"
						/>
					</div>
				{/each}
			</div>
		</div>
	</div>
{/if}

{#if showModal}
	<div
		class="bg-gray bg-opacity-75 fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm"
		on:click={closeModal}
		aria-hidden="true"
	>
		<img
			src={images[image]}
			class="m-3 max-h-[90%] max-w-[90%] rounded-md object-contain shadow-lg"
			alt="Post"
		/>
		{#if images.length > 1}
			<div class="absolute inset-0 flex items-center justify-between px-5">
				<button
					on:click|stopPropagation={prevImage}
					class="bg-opacity-25 hover:bg-opacity-50 rounded-full bg-black p-2 text-3xl text-white transition duration-200"
				>
					&#8592;
				</button>
				<button
					on:click|stopPropagation={nextImage}
					class="bg-opacity-25 hover:bg-opacity-50 rounded-full bg-black p-2 text-3xl text-white transition duration-200"
				>
					&#8594;
				</button>
			</div>
			<div class="bg-opacity-50 absolute right-2 bottom-2 rounded-lg bg-black p-2 text-white">
				<span>{image + 1}/{images.length}</span>
			</div>
		{/if}
	</div>
{/if}

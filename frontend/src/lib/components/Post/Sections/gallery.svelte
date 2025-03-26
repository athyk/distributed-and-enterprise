<script lang="ts">
    import { onMount } from "svelte";
    export let images: string[] = [];

    let image: number = 0;
    let showModal = false;

    let hasLoadedImages = false;

    function removeInvalidImages() {
        images = images.filter((image) => {
            const img = new Image();
            img.src = image;
            return img.complete;
        });
        if (images.length > 0) {
            hasLoadedImages = true;
        } else {
            hasLoadedImages = false;
        }
    }


    function nextImage() {
        image = (image + 1) % images.length;
    }

    function prevImage() {
        image = (image - 1 + images.length) % images.length;
    }

    function openModal(event: MouseEvent) {
        console.log("openModal", image);
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
            if (event.key === "ArrowRight") {
                nextImage();
            } else if (event.key === "ArrowLeft") {
                prevImage();
            } else if (event.key === "Escape") {
                closeModal();
            }
        }
    }

    window.addEventListener("keydown", handleKeydown);

    onMount(() => {
        removeInvalidImages();
    });

</script>

{#if images.length > 0}
    <div class="relative flex flex-col items-center overflow-hidden">
        <div class="w-full max-w-2xl p-2">
            <div class="flex flex-row gap-2 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-100">
                {#each images as image, i (i)}
                    <div class="flex-shrink-0" on:click={openModal}  aria-hidden="true" id={i.toString()}>
                        <img
                            src={image}
                            alt="User uploaded"
                            class="h-[100px] w-auto object-cover rounded hover:cursor-pointer hover:opacity-75 hover:shadow-lg transition duration-200"
                        />
                    </div>
                {/each}
            </div>
        </div>
    </div>
{/if}

{#if showModal}
    <div class="fixed inset-0 bg-gray bg-opacity-75 backdrop-blur-sm flex items-center justify-center z-50"
        on:click={closeModal}
        aria-hidden="true"
    >
        <img
            src={images[image]}
            class="max-w-[90%] max-h-[90%] object-contain shadow-lg rounded-md m-3"
            alt="Post"
        />
        {#if images.length > 1}
            <div class="absolute inset-0 flex justify-between items-center px-5">
                <button on:click|stopPropagation={prevImage} class="text-3xl bg-black bg-opacity-25 rounded-full p-2 hover:bg-opacity-50 transition duration-200 text-white">
                    &#8592;
                </button>
                <button on:click|stopPropagation={nextImage} class="text-3xl bg-black bg-opacity-25 rounded-full p-2 hover:bg-opacity-50 transition duration-200 text-white">
                    &#8594;
                </button>
            </div>
            <div class="absolute bottom-2 right-2 p-2 bg-black bg-opacity-50 text-white rounded-lg">
                <span>{image + 1}/{images.length}</span>
            </div>
        {/if}
    </div>
{/if}
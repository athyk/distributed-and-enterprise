<script lang="ts">
    export let images_urls = [] as string[];

    let image = 0;

    function nextImage() {
        image = (image + 1) % images_urls.length;
    }

    function prevImage() {
        image = (image - 1 + images_urls.length) % images_urls.length;
    }

</script>

<div class="relative flex flex-col items-center">
    <img src={images_urls[image]} class="w-full h-auto shadow-2xl rounded-lg m-5 mb-0" alt="Post" />
    {#if images_urls.length > 1}
        <div class="absolute inset-0 flex justify-between items-center px-5">
            <button on:click={prevImage} class="text-3xl bg-opacity-5 rounded-2xl p-1 hover:bg-gray-900 transition duration-200 text-white">
                &#8592;
            </button>
            <button on:click={nextImage} class="text-3xl bg-opacity-5 rounded-2xl p-1 hover:bg-gray-900 transition duration-200 text-white">
                &#8594;
            </button>
        </div>
        <div class="absolute bottom-0 right-0 p-2 bg-black bg-opacity-50 text-white rounded-tl-lg">
            <span>{image + 1}/{images_urls.length}</span>
        </div>
    {/if}
</div>

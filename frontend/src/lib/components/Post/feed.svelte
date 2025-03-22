<script lang="ts">
    import Create from "$components/Post/create.svelte";


    import Masonry from 'svelte-bricks';
    import { onMount } from "svelte";
    export let items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];



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

    let showCreateModal = false;

    function toggleCreateModal() {
        showCreateModal = !showCreateModal;
    }

    function closeCreateModal() {
        showCreateModal = false;
    }


</script>




<div class="w-full flex flex-wrap justify-center">

    <button
        type="button"
        class="fixed bottom-4 right-4 w-16 h-16 bg-blue-500 text-white rounded-full flex items-center justify-center shadow-lg hover:bg-blue-700 z-40"
        on:click={toggleCreateModal}
        aria-label="Open create modal"
    >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
    </button>

    {#if showCreateModal}
        <div class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
            <div class="bg-white rounded-lg w-full max-w-3xl max-h-[90vh] overflow-y-auto relative">
                <button 
                    class="absolute top-2 right-2 text-gray-500 hover:text-gray-800"
                    on:click={closeCreateModal}
                    aria-label="Close create modal"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
                <div class="p-6">
                    <Create on:close={closeCreateModal} />
                </div>
            </div>
        </div>
    {/if}


    <Masonry
        items={[items]}
        minColWidth={minColWidth}
        maxColWidth={maxColWidth}
        gap={gap}
        masonryWidth={width}
        masonryHeight={height}
    >
        <slot name="Posts" />
    </Masonry>
</div>
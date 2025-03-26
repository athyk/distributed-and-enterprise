<script lang="ts">
    import CreatePost from "$components/Post/create.svelte";

    type PostType = 'posts' | 'events' | 'announcements';
    export let feedType: PostType = 'posts';
    export let showActions = true;

    let refreshKey = 0;

    let modalShown = false;

    function showModal() {
        modalShown = true;
    }

    function hideModal() {
        modalShown = false;
        refreshKey += 1;
    }
</script>

<div class="w-full flex flex-wrap justify-center">
    {#if showActions}
        <button
            type="button"
            class="fixed bottom-4 right-4 w-16 h-16 bg-blue-500 text-white rounded-full flex items-center justify-center shadow-lg hover:bg-blue-700 z-40"
            on:click={showModal}
            aria-label="Open create modal"
        >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
        </button>
        {#if modalShown}
            {#if feedType === 'posts'}
                <div class="fixed inset-0 bg-gray bg-opacity-75 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <CreatePost on:close={hideModal} bind:showModal={modalShown} />
                </div>

            {:else if feedType === 'events'}
                <!-- <h1>Events</h1> -->
            {:else if feedType === 'announcements'}
                <!-- <h1>Announcements</h1> -->
            {/if}
        {/if}
    {/if}
    {#key refreshKey}
        <slot  name="Posts" />
    {/key}
</div>
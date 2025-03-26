<script lang="ts">
    import CreatePost from "$components/Post/createPost.svelte";
    import { onMount, onDestroy } from 'svelte';

    type PostType = 'posts' | 'events' | 'announcements';
    export let feedType: PostType = 'posts';
    export let showActions = true;

    let refreshKey = 0;

    let modalShown = false;
    let editShown = false;
    let editID = 0;
    let communityID = 1;

    function showModal() {
        modalShown = true;
    }

    function hideModal() {
        modalShown = false;
        refreshKey += 1;
    }

    function showEditModal(id: number,commID: number = 1) {
        editShown = true;
        editID = id;
        modalShown = true;
        commID = communityID;
        console.log("Edit modal shown for post ID:", id);
    }

    function handleEditPost(event: CustomEvent) {
        console.log("Edit post event received:", event);
        if (event.detail && event.detail.id) {
            showEditModal(event.detail.id, event.detail.communityID);
        }
    }

    onMount(() => {
        document.addEventListener('editpost', handleEditPost as EventListener);
    });

    onDestroy(() => {
        document.removeEventListener('editpost', handleEditPost as EventListener);
    });

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
                    <CreatePost
                        bind:showModal={modalShown}
                        edit={editShown}
                        editID={editID}
                        onClose={() => hideModal()}
                        onSuccess={() => refreshKey += 1}
                    />
                </div>

            {:else if feedType === 'events'}
                <h1>TBD</h1>
            {:else if feedType === 'announcements'}
                <div class="fixed inset-0 bg-gray bg-opacity-75 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                    <CreatePost
                        bind:showModal={modalShown}
                        edit={editShown}
                        editID={editID}
                        onClose={() => hideModal()}
                        onSuccess={() => refreshKey += 1}
                        annnoucement={true}
                        communityID={communityID}
                    />
                </div>
            {/if}
        {/if}
    {/if}
    {#key refreshKey}
        <slot  name="Posts" />
    {/key}
</div>
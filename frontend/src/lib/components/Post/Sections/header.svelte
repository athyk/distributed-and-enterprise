<script lang="ts">
    import type { UserInfo } from "$lib/api/apiType";
    import { isUserID }  from "$lib/api/checkUser";
	import { onMount } from "svelte";
    export let author: UserInfo = {} as UserInfo;
    export let id = 0 as number;
    let ownPost = false as boolean;

    async function isAuthor() {
        return await isUserID(author.user_id);
    }

    onMount(() => {
        isAuthor().then((result) => {
            ownPost = result;
        });
    });

    function handleEdit() {
        console.log('Sending edit event for post ID:', id);
        const event = new CustomEvent('editpost', {
            bubbles: true,
            detail: { id }
        });
        console.log('Dispatching event:', event);
        document.dispatchEvent(event);
        showdropdown = false;
    }

    function handleDelete() {
        console.log('Sending delete event for post ID:', id);
        const event = new CustomEvent('deletePost', {
            bubbles: true,
            detail: { id }
        });
        console.log('Dispatching event:', event);
        document.dispatchEvent(event);
    }

    let showdropdown = false;
</script>

<div class="flex items-center space-x-2 top-0 bg-white p-2 rounded-t-2xl" id={'header-' + id.toString()}>
    {#if author.picture_url}
        <a href={author.user_id.toString()} target="_blank" rel="noopener noreferrer">
            <img src={author.picture_url} alt="Profile Icon" class="h-11 w-11 rounded-full" />
        </a>
    {/if}
    <span class="font-bold">{author.first_name} {author.last_name}</span>
    {#if ownPost}
        <span class="text-gray-500 text-sm">(You)</span>
    {/if}

    {#if ownPost}
        <span class="flex items-center space-x-2 ml-auto">
            <div class="relative">
                <button type="button" class="text-black hover:text-gray-700 transition duration-200 cursor-pointer" aria-label="More options"  onclick="{() => showdropdown = !showdropdown}">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v.01M12 12v.01M12 18v.01" />
                    </svg>
                </button>
                <div class="absolute right-0 bg-gray-500  w-40 rounded-xl {showdropdown ? 'block' : 'hidden'} shadow-lg">
                    <ul class="ml-2 my-1 bg-gray-500 text-white rounded-xl p-2 space-y-2">
                        <li>
                            <button class="hover:bg-gray-600 rounded-lg p-2 w-full text-left" onclick={handleEdit}>Edit</button>
                        </li>
                        <li>
                            <button class="hover:bg-gray-600 rounded-lg p-2 w-full text-left" onclick={handleDelete}>Delete</button>
                        </li>
                    </ul>
                </div>
            </div>
        </span>
    {/if}

</div>
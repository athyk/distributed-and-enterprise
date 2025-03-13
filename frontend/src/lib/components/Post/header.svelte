<script lang="ts">
    export let author = '' as string;
    export let ownPost = false as boolean;
    let showdropdown = false;
</script>

<div class="flex items-center space-x-2 sticky top-0 bg-gray-300 p-2 rounded-t-2xl">
    <svg height="40" width="40" xmlns="http://www.w3.org/2000/svg">
        <circle r="20" cx="20" cy="20" fill="black" />
    </svg>
    <span class="font-bold">{author}</span>

    {#if ownPost}
        <span class="flex items-center space-x-2 ml-auto">
            <div class="relative">
                <button type="button" class="text-black hover:text-gray-700 transition duration-200 cursor-pointer" aria-label="More options"  onclick="{() => showdropdown = !showdropdown}">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v.01M12 12v.01M12 18v.01" />
                    </svg>
                </button>
                <div class="absolute right-0 bg-gray-500  w-40 rounded-xl {showdropdown ? 'block' : 'hidden'} shadow-lg">
                    <ul class="ml-2 my-1 bg-gray-500 text-white rounded-xl p-2">
                        <li class="hover:bg-gray-600 rounded-lg p-2">Edit</li>
                    </ul>
                </div>
            </div>
        </span>
    {/if}

</div>
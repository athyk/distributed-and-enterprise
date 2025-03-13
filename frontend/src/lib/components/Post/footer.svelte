<script lang="ts">
    export let likes = 0 as number;
    export let date = '' as string;
    export let showLikes = true as boolean;

    let liked = false;

    function likePost() {
        if (liked) {
            likes--;
            liked = false;
        } else {
            likes++;
            liked = true;
        }
    }

    function convertTimestamp(timestamp: string) {
        const date = new Date(parseInt(timestamp) * 1000);
        const options: Intl.DateTimeFormatOptions = {
            hour: 'numeric',
            minute: 'numeric',
            hour12: true,
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        };
        let formattedDate = date.toLocaleString('en-GB', options);
        return formattedDate;
    }
</script>

<div class="flex items-center space-x-2 justify-between">
    {#if date}
        <span class="text-black text-sm">Posted at {convertTimestamp(date)}</span>
    {/if}
    {#if showLikes}
        <span class="flex items-center space-x-2">
            <button type="button" class="h-7 w-7 {liked ? 'text-red-500' : 'text-black-500'} hover:text-red-500 transition duration-200 cursor-pointer" aria-label="Like post"
                onclick="{likePost}">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
                </svg>
            </button>
            <span>{likes}</span>
        </span>
    {/if}
</div>
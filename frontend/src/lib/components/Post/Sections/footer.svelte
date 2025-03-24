<script lang="ts">
    import { convertTimestamp } from "$lib/utils/unixToSring";
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
</script>

<div class="flex items-center space-x-2 justify-between mt-3">
    {#if date}
        <span class="text-black text-sm">Posted at {convertTimestamp(date)}</span>
    {/if}
</div>
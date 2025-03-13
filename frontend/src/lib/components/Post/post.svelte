<script lang="ts">
    import Header from "./header.svelte";
    import Footer from "./footer.svelte";

    export let author = '' as string;
    export let date = '' as string;
    export let id = 0 as number;
    export let likes = 0 as number;
    export let showLikes = true as boolean;
    export let ownPost = false as boolean;




</script>


<div class="flex flex-col justify-between min-h-[400px] bg-gray-300 rounded-2xl border-black border-1 m-5 p-5" id={id.toString()}>
    <Header author={author} ownPost={ownPost} />

    <slot />

    <Footer likes={likes} date={date} showLikes={showLikes} />
</div>
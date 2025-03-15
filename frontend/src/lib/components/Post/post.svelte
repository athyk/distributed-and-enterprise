<script lang="ts">
    import Header from "./Sections/header.svelte";
    import Footer from "./Sections/footer.svelte";
    export let author: {
        name: string,
        profile_image: string,
        URL: string,
        DegreeYear?: string,
        Degree?: string,
    };
    export let date = '' as string;
    export let id = 0 as number;
    export let likes = 0 as number;
    export let showLikes = true as boolean;
    export let ownPost = false as boolean;
</script>

<div class="flex flex-col justify-between min-h-[50px] bg-gray-300 rounded-2xl border-black border-1 m-5 p-5" id={id.toString()}>
    <Header {author} {ownPost} />

    <slot />

    <Footer likes={likes} date={date} showLikes={showLikes} />
</div>
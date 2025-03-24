<script lang="ts">
    import Header from "./Sections/header.svelte";
    import Footer from "./Sections/footer.svelte";
	import type { UserInfo } from "$lib/api/apiType";

    export let author: UserInfo = {} as UserInfo;
    export let date = '' as string;
    export let id = 0 as number;
    export let ownPost = false as boolean;
</script>

<div class="flex flex-col justify-between min-h-[50px] min-w-[100px] max-w-[500px] bg-white rounded-2xl border-black border-1 m-5 p-5" id={id.toString()}>
    <Header {author} {ownPost} />

    <slot />

    <Footer date={date}/>
</div>
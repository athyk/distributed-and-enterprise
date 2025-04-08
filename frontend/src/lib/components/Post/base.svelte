<script lang="ts">
	import Header from './Sections/header.svelte';
	import Footer from './Sections/footer.svelte';
	import type { UserInfo } from '$lib/api/apiType';

	export let author: UserInfo = {} as UserInfo;
	export let date = '' as string;
	export let id = 0 as number;
	export let communityID = 0 as number;
</script>


<div
	class="mx-auto my-3 flex w-full max-w-[500px] flex-col justify-between rounded-2xl shadow-xl bg-white p-3 sm:m-2 sm:p-5"
	id={id.toString()}
>
	<Header {author} {id} {communityID} />

	<slot />

	<Footer {date} />
</div>

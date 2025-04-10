<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import { isLoggedIn } from '$lib/api/checkUser';

	import CreateEditPost from '$components/Post/CreateEdit/Edit-Create-Post.svelte';
	import CreateEditAnnoucement from '$components/Post/CreateEdit/Edit-Create-Annoucement.svelte';
	import CreateEditEvent from '$components/Post/CreateEdit/Edit-Create-Event.svelte';

	type PostType = 'posts' | 'events' | 'announcements';
	export let feedType: PostType = 'posts';
	export let showActions = true;
	export let feedClass = 'flex w-full flex-wrap justify-center';
	export let communityID = 1;

	let refreshKey = 0;

	let modalShown = true;
	let editShown = false;
	let editID = 0;

	let scrollTimeout: ReturnType<typeof setTimeout> | null = null;

	function showModal() {
		modalShown = true;
	}

	function hideModal() {
		modalShown = false;
		refreshKey += 1;
	}

	function showEditModal(id: number, commID: number = 1) {
		editShown = true;
		editID = id;
		modalShown = true;
		communityID = commID;
		console.log('Edit modal shown for post ID:', id);
	}

	function handleEditPost(event: CustomEvent) {
		console.log('Edit post event received:', event);
		if (event.detail && event.detail.id) {
			showEditModal(event.detail.id, event.detail.communityID);
		}
	}

	function handleScroll() {
		if (!browser) return;
		if (scrollTimeout) return;

		const { scrollTop, scrollHeight, clientHeight } = document.documentElement || document.body;

		if (scrollTop + clientHeight >= scrollHeight - 500) {
			document.dispatchEvent(new CustomEvent('scrollbottomreach'));
			scrollTimeout = setTimeout(() => (scrollTimeout = null), 1000);
		}


	}

	type EditPostEvent = CustomEvent<{ id: number; communityId?: number }>;
	const eventHandler = (e: Event) => handleEditPost(e as EditPostEvent);

	onMount(() => {
		if (browser) {
			document.addEventListener('editpost', eventHandler);
			document.addEventListener('scroll', handleScroll);
		}
		isLoggedIn().then((result) => {
			if (!result) {
				showActions = false;
			}
		});
	});

	onDestroy(() => {
		if (browser) {
			document.removeEventListener('editpost', eventHandler);
			document.removeEventListener('scroll', handleScroll);
		}
	});
</script>


<div class={feedClass}>
	{#if showActions}
		<button
			type="button"
			class="fixed right-4 bottom-4 z-40 flex h-16 w-16 items-center justify-center rounded-full bg-blue-500 text-white shadow-lg hover:bg-blue-700"
			on:click={showModal}
			aria-label="Open create modal"
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
				stroke-width="1.5"
				stroke="currentColor"
				class="h-8 w-8"
			>
				<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
			</svg>
		</button>
		{#if modalShown}
		<div
			class="bg-gray bg-opacity-75 fixed inset-0 z-50 flex items-center justify-center p-4 backdrop-blur-sm"
		>
			{#if feedType === 'posts'}
				<CreateEditPost
					bind:showModal={modalShown}
					onClose={() => hideModal()}
					onSuccess={() => (refreshKey += 1)}
					edit={editShown}
					editID={editID}
				/>
			{:else if feedType === 'events'}
				<CreateEditEvent
					bind:showModal={modalShown}
					onClose={() => hideModal()}
					onSuccess={() => (refreshKey += 1)}
					edit={editShown}
					editID={editID}
					communityID={communityID}
				/>
			{:else if feedType === 'announcements'}
				<CreateEditAnnoucement
					bind:showModal={modalShown}
					onClose={() => hideModal()}
					onSuccess={() => (refreshKey += 1)}
					edit={editShown}
					editID={editID}
					communityID={communityID}
				/>
			{/if}
		</div>
		{/if}
	{/if}
	{#key refreshKey}
		<slot name="Posts" />
	{/key}
</div>
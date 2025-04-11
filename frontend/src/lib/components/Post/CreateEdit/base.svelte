<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';

	import Base from '../base.svelte';
	import Title from '../Sections/title.svelte';
	import { isLoggedIn } from '$lib/api/checkUser';

	export let ModalTitle = '' as string;
	export let showModal = false;
	export let ButtonText = 'Submit' as string;
	export let onClose = () => {};
	export let onSubmit = () => {};

	function closeModal() {
		showModal = false;
		onClose();
	}

	function handleKeydown(event: KeyboardEvent) {
		if (showModal) {
			if (event.key === 'Escape') {
				closeModal();
			}
		}
	}

	async function checkUserPermission() {
		if ((await isLoggedIn()) === false) {
			console.log('User is not logged in');
			showModal = false;
			return false;
		}
		console.log('User is logged in');
		return true;
	}

	onMount(() => {
		if (browser) {
			window.addEventListener('keydown', handleKeydown);
		}
		checkUserPermission();
	});

	onDestroy(() => {
		if (browser) {
			window.removeEventListener('keydown', handleKeydown);
		}
	});
</script>

<Base>
	<Title>{ModalTitle}</Title>
	<slot name="content" />
	<div
		class="mt-2 flex w-full items-center justify-between rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
	>
		<button
			class="rounded bg-green-500 px-4 py-2 text-white"
			on:click|preventDefault|stopPropagation={onSubmit}
		>
			{ButtonText}
		</button>
		<slot name="actions" />
		<button class="rounded bg-red-500 px-4 py-2 text-white" on:click={closeModal}> Close </button>
	</div>
</Base>

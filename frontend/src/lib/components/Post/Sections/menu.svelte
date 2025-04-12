<script lang="ts">
	import type { UserInfo } from '$lib/api/apiType';
	import { isUserID, checkPermisions } from '$lib/api/checkUser';
	import { onMount } from 'svelte';

	export let author: UserInfo = {} as UserInfo;
	export let id = 0 as number;
	export let communityID = 0 as number;
	let ownPost = false as boolean;
	let showdropdown = false;

	async function isAuthor() {
		if (communityID !== 0) {
			const response = await checkPermisions(communityID);
			if (response) {
				return true;
			}
		}
		return await isUserID(author.user_id, true);
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
			detail: { id, communityId: communityID }
		});
		console.log('Dispatching event:', event);
		document.dispatchEvent(event);
		showdropdown = false;
	}

	function handleDelete() {
		console.log('Sending delete event for post ID:', id);
		const event = new CustomEvent('deletePost', {
			bubbles: true,
			detail: { id, communityId: communityID }
		});
		console.log('Dispatching event:', event);
		document.dispatchEvent(event);
	}
</script>

{#if ownPost}
	<span class="ml-auto flex items-center space-x-2">
		<div class="relative">
			<button
				type="button"
				class="cursor-pointer text-black transition duration-200 hover:text-gray-700"
				aria-label="More options"
				onclick={() => (showdropdown = !showdropdown)}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					class="h-6 w-6"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M12 6v.01M12 12v.01M12 18v.01"
					/>
				</svg>
			</button>
			<div
				class="absolute right-0 w-40 rounded-xl bg-gray-500 {showdropdown
					? 'block'
					: 'hidden'} shadow-lg"
			>
				<ul class="my-1 ml-2 space-y-2 rounded-xl bg-gray-500 p-2 text-white">
					<li>
						<button class="w-full rounded-lg p-2 text-left hover:bg-gray-600" onclick={handleEdit}
							>Edit</button
						>
					</li>
					<li>
						<button class="w-full rounded-lg p-2 text-left hover:bg-gray-600" onclick={handleDelete}
							>Delete</button
						>
					</li>
				</ul>
			</div>
		</div>
	</span>
{/if}

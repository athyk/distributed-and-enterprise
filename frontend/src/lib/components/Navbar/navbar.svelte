<script lang="ts">
	import { onMount } from 'svelte';
	import { isLoggedIn } from '$lib/api/checkUser';
	import { post } from '$lib/api/post';
	import type { response } from '$lib/api/apiType';

	let isOpen = false;
	let LoggedIn = false;

	function toggleMenu() {
		isOpen = !isOpen;
	}

	async function logout() {
		console.log('Logging out...');
		let response = (await post('auth/logout', {})) as response;
		if (response.success === true) {
			localStorage.setItem('loggedin', 'false');
			window.location.href = '/login';
		} else {
			console.error('Logout failed');
		}
	}

	onMount(() => {
		if (localStorage.getItem('loggedin') === 'true') {
			isLoggedIn().then((result) => {
				localStorage.setItem('loggedin', result.toString());
			});
		}
		if (localStorage.getItem('loggedin') === 'true') {
			urls = {
				Communities: '/communities',
				Account: '/account',
				Logout: ''
			};
			LoggedIn = true;
		} else {
			urls = {
				Login: '/login'
			};
		}
	});

	let urls: { [key: string]: string } = {
		Login: '/login'
	};
</script>

<nav class="bg-gray-800 p-4">
	<div class="container mx-auto flex items-center justify-between">
		<a href="/" class="text-[35px] font-semibold text-white">UniHub</a>
		<button class="text-white md:hidden" on:click={toggleMenu} aria-label="Toggle menu">
			<svg
				class="h-6 w-6"
				fill="none"
				stroke="currentColor"
				viewBox="0 0 24 24"
				xmlns="http://www.w3.org/2000/svg"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M4 6h16M4 12h16m-7 6h7"
				></path>
			</svg>
		</button>
		<div class="hidden space-x-4 md:flex">
			{#each Object.keys(urls) as url}
				{#if url !== 'Logout'}
					<a href={urls[url]} class="text-[20px] text-gray-300 hover:text-white">{url}</a>
				{/if}
				{#if LoggedIn && url === 'Logout'}
					<button
						type="button"
						class="text-[20px] text-gray-300 hover:text-white"
						on:click={logout}
						aria-label="Logout"
					>
						Logout
					</button>
				{/if}
			{/each}
		</div>
	</div>
	<div class={`mt-5  rounded bg-gray-600 pl-3 md:hidden ${isOpen ? 'block' : 'hidden'}`}>
		{#each Object.keys(urls) as url}
			{#if url !== 'Logout'}
				<a href={urls[url]} class="block p-2 text-gray-300 hover:text-white">{url}</a>
			{/if}
			{#if LoggedIn && url === 'Logout'}
				<button
					type="button"
					class="block w-full p-2 text-left text-gray-300 hover:text-white"
					on:click={logout}
					aria-label="Logout"
				>
					Logout
				</button>
			{/if}
		{/each}
	</div>
</nav>

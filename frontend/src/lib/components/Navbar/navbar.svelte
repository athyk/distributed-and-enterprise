<script lang="ts">
	import { onMount } from 'svelte';
	import { isLoggedIn } from '$lib/api/checkUser';

	let isOpen = false;
	let LoggedIn = false;

	function toggleMenu() {
		isOpen = !isOpen;
	}

	onMount(() => {
		if (localStorage.getItem('loggedin') === 'true') {
			isLoggedIn().then(result => {
				localStorage.setItem('loggedin', result.toString());
			});
		}
		if (localStorage.getItem('loggedin') === 'true') {
			console.log('2 | LoggedIn:', LoggedIn);
			urls = {
				Posts: '/posts',
				Communities: '/communities',
				Account: '/account',
				Logout: '/logout',
			};
			LoggedIn = true;
		}
	});

	let urls: { [key: string]: string } = {
		Login: '/login',
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
				<a href={urls[url]} class="text-[20px] text-gray-300 hover:text-white">{url}</a>
			{/each}
		</div>
	</div>
	<div class={`mt-5  rounded bg-gray-600 pl-3 md:hidden ${isOpen ? 'block' : 'hidden'}`}>
		{#each Object.keys(urls) as url}
			<a href={urls[url]} class="block p-2 text-gray-300 hover:text-white">{url}</a>
		{/each}
	</div>
</nav>

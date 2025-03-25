<script lang="ts">
	import SideBar from '$components/Sidebar/sidebar.svelte';
	import { onMount, onDestroy } from 'svelte';

	let { children } = $props();
	let isSidebarOpen = false;
	let isMobile = false;

	// Function to check if the screen size is mobile
	function handleResize() {
		isMobile = window.innerWidth < 768;
		if (!isMobile) {
			isSidebarOpen = false; // Close sidebar when switching to desktop view
		}
	}

	// Toggle sidebar visibility
	function toggleSidebar() {
		isSidebarOpen = !isSidebarOpen;
	}

	// Close sidebar
	function closeSidebar() {
		isSidebarOpen = false;
	}

	/*
	onMount(() => {
		handleResize();
		window.addEventListener('resize', handleResize);
	});

	onDestroy(() => {
		window.removeEventListener('resize', handleResize);
	});

	*/
</script>

<div class="flex min-h-screen flex-col text-gray-900 dark:text-gray-100">
	<!-- Mobile Filter Button (Under Header) -->
	<div class="bg-gray-100 px-4 py-2 shadow md:hidden dark:bg-gray-900">
		<button
			class="w-full rounded-lg bg-blue-600 px-4 py-2 text-white shadow-lg"
			on:click={toggleSidebar}
		>
			Filter
		</button>
	</div>

	<!-- Sidebar & Page Content -->
	<div class="relative flex flex-1">
		<!-- Sidebar for Large Screens -->
		<div class="hidden w-64 md:block">
			<SideBar />
		</div>

		<!-- Mobile Sidebar Overlay -->
		{#if isSidebarOpen}
			<div
				class="bg-opacity-50 fixed inset-0 z-40 bg-black md:hidden"
				on:click={closeSidebar}
				aria-label="Close sidebar"
			></div>
		{/if}

		<!-- Sidebar for Mobile -->
		<div
			class="fixed inset-y-0 left-0 z-50 w-64 transform overflow-y-auto bg-white transition-transform duration-300 ease-in-out dark:bg-gray-800"
			class:translate-x-0={isSidebarOpen}
			class:-translate-x-full={!isSidebarOpen}
		>
			<SideBar />
		</div>

		<!-- Page Content -->
		<main class="flex-1 overflow-auto p-6">
			{@render children()}
		</main>
	</div>
</div>

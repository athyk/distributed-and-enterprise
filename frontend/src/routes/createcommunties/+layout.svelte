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
			isSidebarOpen = false;  // Close sidebar when switching to desktop view
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

	onMount(() => {
		handleResize();
		window.addEventListener('resize', handleResize);
	});

	onDestroy(() => {
		window.removeEventListener('resize', handleResize);
	});
</script>

<div class="min-h-screen flex flex-col text-gray-900 dark:text-gray-100">
	<!-- Mobile Filter Button (Under Header) -->
	<div class="md:hidden px-4 py-2 bg-gray-100 dark:bg-gray-900 shadow">
		<button
			class="w-full bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg"
			on:click={toggleSidebar}
		>
			Filter
		</button>
	</div>

	<!-- Sidebar & Page Content -->
	<div class="flex flex-1 relative">
		<!-- Sidebar for Large Screens -->
		<div class="hidden md:block w-64">
			<SideBar />
		</div>

		<!-- Mobile Sidebar Overlay -->
		{#if isSidebarOpen}
			<div
				class="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
				on:click={closeSidebar}
				aria-label="Close sidebar"
			></div>
		{/if}

		<!-- Sidebar for Mobile -->
		<div 
			class="fixed inset-y-0 left-0 z-50 w-64 bg-white dark:bg-gray-800 overflow-y-auto transition-transform duration-300 ease-in-out transform"
			class:translate-x-0={isSidebarOpen}
			class:-translate-x-full={!isSidebarOpen}
		>
			<SideBar />
		</div>

		<!-- Page Content -->
		<main class="flex-1 p-6 overflow-auto">
			{@render children()}
		</main>
	</div>
</div>

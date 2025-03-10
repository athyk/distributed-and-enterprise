<script lang="ts">

	import NavBar from '$components/Navbar/navbar.svelte';
    import SideBar from '$components/Sidebar/sidebar.svelte';
	let { children } = $props();
</script>

<!-- Layout -->
<div class="min-h-screen flex flex-col text-gray-900 dark:text-gray-100">
    <!-- Top Navigation -->


    <!-- Main Content Wrapper -->
    <div class="flex flex-1">
        <!-- Sidebar (Collapsible) -->
        <SideBar />

        <!-- Page Content -->
        <main class="flex-1 p-6 overflow-auto">
            {@render children()}
        </main>
    </div>
</div>

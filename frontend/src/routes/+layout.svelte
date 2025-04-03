<script lang="ts">
	import '../app.css';
	let { children } = $props();
	import NavBar from '$components/Navbar/navbar.svelte';



</script>

<NavBar />
{@render children()}

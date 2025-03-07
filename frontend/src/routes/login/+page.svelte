<script lang="ts">
	import LoginCard from '$components/LoginCard/LoginCard.svelte';
</script>

<div class="flex h-screen w-full items-center justify-center">
	<div
		class="mx-auto mt-5 flex h-[50vh] w-1/2 overflow-hidden rounded-lg border-1 border-black bg-white shadow-lg"
	>
		<div
			class="hidden w-1/3 bg-cover md:block"
			style="background-image: url('https://images.unsplash.com/photo-1521587760476-6c12a4b040da?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')"
		></div>
		<LoginCard />
	</div>
</div>

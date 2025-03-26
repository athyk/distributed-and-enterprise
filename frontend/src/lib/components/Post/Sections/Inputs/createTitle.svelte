<script lang="ts">
	export let title: string = '';
</script>

<input
	type="text"
	bind:value={title}
	placeholder="Title"
	class="w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
	required
/>

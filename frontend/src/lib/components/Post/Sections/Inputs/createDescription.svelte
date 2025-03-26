<script lang="ts">
	export let text: string = '';
</script>

<textarea
	bind:value={text}
	placeholder="Description"
	class="mt-2 h-[155px] w-full rounded-lg border-2 border-gray-300 p-2 focus:border-blue-500 focus:outline-none"
	required
></textarea>

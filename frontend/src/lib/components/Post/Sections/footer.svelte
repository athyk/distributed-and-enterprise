<script lang="ts">
	import { convertTimestamp } from '$lib/utils/unixToSring';
	export let date = '' as string;
</script>

<div class="mt-3 flex items-center justify-between space-x-2">
	{#if date}
		<span class="text-sm text-black">Posted at {convertTimestamp(date)}</span>
	{/if}
</div>

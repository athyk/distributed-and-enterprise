<script lang="ts">
	export let datetime = '' as string;
	export let duration = '' as string;

	function convertTimestamp(timestamp: string): string {
		const date = new Date(timestamp);
		return date.toLocaleString('en-US', {
			month: 'short',
			day: '2-digit',
			year: 'numeric',
			hour: '2-digit',
			minute: '2-digit',
			hour12: true
		});
	}

	$: datetime = convertTimestamp(datetime);
</script>

<div
	class="scrollbar-thin scrollbar-thumb-gray-500 scrollbar-track-gray-200 flex space-x-2 overflow-x-auto py-2 whitespace-nowrap"
>
	{datetime}
	{#if duration !== ''}
		<span class="pl-1 text-gray-500"> ({duration} hours)</span>
	{/if}
</div>

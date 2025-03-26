<script lang="ts">
    export let datetime = '' as string;

    function convertTimestamp(timestamp: string): string {
        const date = new Date(timestamp);
        return date.toLocaleString('en-US', {
            month: 'short',
            day: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true,
        });
    }

    $: datetime = convertTimestamp(datetime);


</script>

<div class="flex space-x-2 overflow-x-auto whitespace-nowrap scrollbar-thin scrollbar-thumb-gray-500 scrollbar-track-gray-200 py-2">
    {datetime}
</div>
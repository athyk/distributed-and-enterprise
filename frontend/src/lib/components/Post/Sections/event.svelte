<script lang="ts">
	import Button from "$components/SubmitButton/button.svelte";
    import { convertTimestamp } from "$lib/utils/unixToSring";
    import Map from "./Map/map.svelte";
    export let event: {
        title: string,
        description: string,
        start_time: string,
        end_time: string,
        location: {
            name: string,
            lat: number,
            lon: number,
        },
    };
</script>

<div>
    <div class="p-2 bg-white rounded-t-2xl border-black border-1">
        <p class="font-bold">{event.title}</p>
        <p class="text-gray-500">Start: {convertTimestamp(event.start_time)}</p>
        <p class="text-gray-500">End: {convertTimestamp(event.end_time)}</p>
    </div>
    <div class="p-2 bg-white  border-black border-1">
        <p class="font-bold">Description</p>
        <p class="text-gray-500">{event.description}</p>
    </div>
    <div class="p-2 bg-white border-black border-1">
        <p class="font-bold">Location</p>
        <p class="text-gray-500">{event.location.name}</p>
        {#if event.location.lat && event.location.lon}
            <Map
                map={{lat: event.location.lat, lon: event.location.lon}}
            />
        {/if}
    </div>
    <div class="p-2 bg-white rounded-b-2xl border-black border-1 flex justify-center">
        <button class="w-full rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-900">Join</button>
    </div>
</div>
<script lang="ts">
    import { onMount, onDestroy } from 'svelte';

    export let map: {
        lat: number,
        lon: number,
    };

    let mapContainer: HTMLElement;
    let leafletMap: any;
    let marker: any;
    let L: any;

    onMount(async () => {
        const leaflet = await import('leaflet');
        L = leaflet.default;
        await import('leaflet/dist/leaflet.css');

        leafletMap = L.map(mapContainer).setView([map.lat, map.lon], 16);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(leafletMap);
        marker = L.marker([map.lat, map.lon]).addTo(leafletMap);
    });

    onDestroy(() => {
        if (leafletMap) leafletMap.remove();
    });

</script>


<div bind:this={mapContainer} class="w-full h-[400px] border-black border-1 rounded-2xl mt-2 mb-2"></div>
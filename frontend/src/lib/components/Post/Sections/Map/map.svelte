<script lang="ts">
    import { onMount, onDestroy, tick } from 'svelte';

    export let lat: number;
    export let lon: number;

    let mapContainer: HTMLElement;
    let leafletMap: any;
    let marker: any;
    let L: any;
    let showModal = false;

    onMount(async () => {
        const leaflet = await import('leaflet');
        L = leaflet.default;
        await import('leaflet/dist/leaflet.css');
    });

    async function initializeMap() {

        await tick();

        if (!leafletMap) {
            leafletMap = L.map(mapContainer).setView([lat, lon], 16);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(leafletMap);
            marker = L.marker([lat,lon]).addTo(leafletMap);
        }
    }

    onDestroy(() => {
        if (leafletMap) leafletMap.remove();
    });
</script>

{#if lat && lon}
    <button
        on:click={() => { showModal = true; initializeMap(); }}
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
    >
        Show Map
    </button>
{/if}

{#if showModal}
    <div
        class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center"
        role="dialog"
        aria-modal="true"
        aria-label="Map modal"
    >
        <button
            on:click={() => showModal = false}
            class="absolute inset-0 w-full h-full bg-transparent"
            aria-label="Close map modal"
        ></button>
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div
            class="bg-white p-4 rounded-lg w-full max-w-lg"
            on:click|stopPropagation
            aria-label="Map modal content"
        >
            <div 
                bind:this={mapContainer}
                class="w-full h-96 border border-black rounded-xl my-2"
            ></div>
            <button 
                on:click={() => showModal = false}
                class="mt-2 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
                Close
            </button>
        </div>
    </div>
{/if}

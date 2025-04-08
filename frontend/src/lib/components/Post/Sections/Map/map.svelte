<script lang="ts">
	import { onMount, onDestroy, tick } from 'svelte';
	import type { Map, Marker } from 'leaflet';

	export let lat: number;
	export let lon: number;

	let mapContainer: HTMLElement;
	let leafletMap: Map | null = null;
	let marker: Marker | null = null;
	let L: typeof import('leaflet') | null = null;
	let showModal = false;

	onMount(async () => {
		const leaflet = await import('leaflet');
		L = leaflet.default;
		await import('leaflet/dist/leaflet.css');
	});

	async function initializeMap() {
		await tick();

		if (leafletMap) {
            leafletMap.remove();
            leafletMap = null;
        }

		if (!leafletMap) {
			leafletMap = L.map(mapContainer).setView([lat, lon], 16);
			L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
				attribution: '© OpenStreetMap contributors'
			}).addTo(leafletMap);
			marker = L.marker([lat, lon]).addTo(leafletMap);
			console.log('Map initialized ' + marker);
		}
	}

	onDestroy(() => {
		if (leafletMap) leafletMap.remove();
	});
</script>

{#if lat && lon}
	<button
		on:click={() => {
			showModal = true;
			initializeMap();
		}}
		class="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
	>
		Show Map
	</button>
{/if}

{#if showModal}
	<div
		class="bg-gray bg-opacity-75 fixed inset-0 z-50 flex items-center justify-center p-4 backdrop-blur-sm"
		role="dialog"
		aria-modal="true"
		aria-label="Map modal"
	>
		<button
			on:click={() => (showModal = false)}
			class="absolute inset-0 h-full w-full bg-transparent"
			aria-label="Close map modal"
		></button>
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<!-- svelte-ignore a11y_no_static_element_interactions -->
		<div
			class="w-full max-w-lg rounded-lg bg-white p-4"
			on:click|stopPropagation
			aria-label="Map modal content"
		>
			<div bind:this={mapContainer} class="my-2 h-96 w-full rounded-xl border border-black"></div>
			<button
				on:click={() => (showModal = false)}
				class="mt-2 rounded bg-red-500 px-4 py-2 text-white hover:bg-red-600"
			>
				Close
			</button>
		</div>
	</div>
{/if}

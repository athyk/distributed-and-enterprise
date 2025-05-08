<script lang="ts">
	import { get } from '$lib/api/get';
	import { browser } from '$app/environment';
	import type { PaginationDataResponse, PaginationData, OSMPlace } from '$lib/api/apiType';
	import { onMount, onDestroy } from 'svelte';
	import Popup from '$components/ErrorPopUp/popup.svelte';

	const instanceId = Math.random().toString(36).substring(2, 9);

	onMount(() => {
		if (!browser) return;
		document.addEventListener('click', handleClickOutside);
	});

	onDestroy(() => {
		if (!browser) return;
		document.removeEventListener('click', handleClickOutside);
	});

	export let Name = 'Search Box';
	export let showLabel = false;
	export let placeholder = 'Search';
	export let url = '';
	export let value = '';
	export let id;
	export let multi_select = false;
	export let max_select = 1;
	export let selected: [string, number][] = [];
	export let location_selected: [string, string, string][] = [];
	export let classStyle =
		'mt-2 flex w-full flex-wrap items-center rounded-md border px-2 py-1 focus-within:border-blue-600 focus-within:ring-1 focus-within:ring-blue-600';
	export let marginTop = 'mt-4';
	export let extraSearchParams = '';
	export let minCharacters = 2;
	export let location = false;

	let last_value = '';
	let showDropdown = false;
	let dropdownItems: PaginationData[] = [];
	let locationDropdownItems: OSMPlace[] = [];
	let errorMessage = '';

	async function locationSearch() {
		if (!value || value.length < 5) {
			return;
		}
		console.log('Location Search: ', value);
		let response = (await get(
			'https://nominatim.openstreetmap.org/search?q=' + value + '&format=jsonv2',
			true,
			false
		)) as OSMPlace[];
		last_value = value;
		locationDropdownItems = response || [];
	}

	async function search() {
		if (value === last_value || value === '' || value.length < minCharacters) {
			return;
		}
		if (location) {
			await locationSearch();
		} else {
			let response = (await get(
				url + '?limit=5&name=' + value + extraSearchParams
			)) as PaginationDataResponse;
			if (response.success != true) {
				console.log('Error fetching data');
				return;
			}
			last_value = value;
			dropdownItems = response.degrees || response.tags || [];
			console.log('Data Given: ', dropdownItems);
		}
		if (dropdownItems.length > 0 || locationDropdownItems.length > 0) {
			showDropdown = true;
		} else {
			showDropdown = false;
		}
	}

	function handleClickOutside(event: MouseEvent) {
		const target = event.target as HTMLElement;
		if (!target.closest(`#searchbox-${instanceId}`)) {
			showDropdown = false;
		}
	}

	function handleButtonClick(item: PaginationData, event: MouseEvent) {
		event.stopPropagation();

		if (multi_select) {
			if (selected.length < max_select) {
				selected = [...selected, [item.name, item.id]];
			} else {
				errorMessage = `You can only select ${max_select} items.`;
			}
		} else {
			value = item.name;
			id = item.id;
			selected = [[item.name, item.id]];
			showDropdown = false;
		}
	}

	function handleLocationClick(item: OSMPlace, event: MouseEvent) {
		event.stopPropagation();
		value = item.display_name;
		location_selected = [[item.lat, item.lon, item.display_name]];
		showDropdown = false;
	}
</script>

<Popup bind:errorMessage />
<div class="relative {marginTop}" id={`searchbox-${instanceId}`}>
	{#if showLabel}
		<label for={`${Name}-${instanceId}`} class="mb-1 block text-gray-700">{Name}</label>
	{/if}
	{#if multi_select && max_select > 1 && showLabel}
		<div class="mt-1 text-xs text-gray-500">
			{selected.length}/{max_select} selected
		</div>
	{/if}

	<div class={classStyle}>
		{#if multi_select && selected.length > 0}
			<div class="flex flex-wrap items-center space-x-2">
				{#each selected as [name, itemId]}
					<div
						class="mb-2 flex items-center rounded-md bg-blue-100 px-2 py-1 text-xs whitespace-nowrap text-blue-800"
					>
						<span>{name}</span>
						<button
							type="button"
							class="ml-1 text-blue-500 hover:text-blue-700"
							on:click={(e) => {
								e.stopPropagation();
								selected = selected.filter((item) => item[1] !== itemId);
							}}
						>
							×
						</button>
					</div>
				{/each}
			</div>
		{/if}

		<input
			type="text"
			{placeholder}
			id={`${Name}-${instanceId}`}
			class="w-full flex-grow py-1 outline-none"
			on:input={search}
			on:click={(e) => {
				e.stopPropagation();
				if (value.length > 0) {
					showDropdown = true;
				} else {
					showDropdown = false;
				}
			}}
			bind:value
		/>
	</div>

	{#if showDropdown}
		<div
			class="absolute z-50 w-full max-w-[300%] rounded border border-gray-200 bg-white shadow-md"
			style="top: calc(100% + 5px); left: 0;"
		>
			{#each dropdownItems as item}
				<button
					type="button"
					class="block w-full px-4 py-2 text-left hover:bg-gray-200 text-sm whitespace-normal break-words"
					class:bg-blue-100={multi_select && selected.some((sel) => sel[1] === item.id)}
					on:click={(e) => handleButtonClick(item, e)}
				>
					{item.name}
				</button>
			{/each}
			{#each locationDropdownItems.slice(0, 5) as item}
				<button
					type="button"
					class="block w-full px-4 py-2 text-left hover:bg-gray-200 text-sm whitespace-normal break-words"
					on:click={(e) => {
						handleLocationClick(item, e);
					}}
				>
					{item.display_name}
				</button>
			{/each}
		</div>
	{/if}
</div>

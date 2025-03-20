<script lang="ts">
    import { get } from "$lib/api/get";
    import type { PaginationDataResponse,PaginationData } from '$lib/api/apiType';
    import { onMount, onDestroy } from 'svelte';


    const instanceId = Math.random().toString(36).substring(2, 9);

    onMount(() => {
        document.addEventListener('click', handleClickOutside);
    });

    onDestroy(() => {
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

    let last_value = '';
    let showDropdown = false;
    let dropdownItems: PaginationData[] = [];

    async function search() {
        if (value === last_value || value === '' || value.length < 2) {
            return;
        }
        let response = (await get(url+'/?limit=5&name='+value)) as PaginationDataResponse;
        if (response.success != true) {
            console.log('Error fetching data');
            return
        }
        last_value = value;
        dropdownItems = response.degrees || response.tags || [];
        console.log('Data Given: ', dropdownItems);
        if (dropdownItems.length > 0) {
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
                alert('Max Select Limit Reached');
            }
        } else {
            value = item.name;
            id = item.id;
            selected = [[item.name, item.id]];
            showDropdown = false;
        }
    }
</script>

<div class="mt-4 relative" id={`searchbox-${instanceId}`}>
    {#if showLabel}
        <label for={`${Name}-${instanceId}`} class="block text-gray-700 mb-1">{Name}</label>
    {/if}
	{#if multi_select && max_select > 1 && showLabel}
		<div class="text-xs text-gray-500 mt-1">
			{selected.length}/{max_select} selected
		</div>
	{/if}

    <div class="mt-2 flex flex-wrap items-center w-full rounded-md border px-2 py-1 focus-within:ring-1 focus-within:ring-blue-600 focus-within:border-blue-600">
		{#if multi_select && selected.length > 0}
			<div class="flex items-center overflow-x-auto space-x-2 scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-200">
				{#each selected as [name, itemId]}
					<div class="bg-blue-100 text-blue-800 px-2 py-1 rounded-md flex items-center text-xs whitespace-nowrap">
						<span>{name}</span>
						<button 
							type="button"
							class="ml-1 text-blue-500 hover:text-blue-700"
							on:click={(e) => {
							e.stopPropagation();
							selected = selected.filter(item => item[1] !== itemId);
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
            class="flex-grow outline-none py-1 min-w-[80px]"
            on:input={search}
            on:click={(e) => {
                e.stopPropagation();
                if (value.length > 0) {
                    showDropdown = true;
                } else {
                    showDropdown = false;
                }
            }}
            bind:value={value}
        />
    </div>



    {#if showDropdown}
        <div
            class="absolute w-full rounded bg-white shadow-md border border-gray-200 z-50" 
            style="top: calc(100% + 5px); left: 0;"
        >
            {#each dropdownItems as item}
                <button
                    type="button"
                    class="block w-full px-4 py-2 text-left hover:bg-gray-200"
                    class:bg-blue-100={multi_select && selected.some(sel => sel[1] === item.id)}
                    on:click={(e) => handleButtonClick(item, e)}
                >
                    {item.name}
                </button>
            {/each}
        </div>
    {/if}
</div>
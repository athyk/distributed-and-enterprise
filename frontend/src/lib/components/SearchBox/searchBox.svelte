<script lang="ts">
    import { onMount } from 'svelte';
    export let Name = "Search Box";
    export let showLabel = false;
    export let data: any[] = [];
    export let chosenItems: string[] = [];
    export let maxItems = 1;
    export let placeholder = "Search...";
    export let dataPromise: Promise<any[]> | null = null;

    let filterData: string[] = data;

    let showDropdown = false;

    onMount(async () => {
        try {
            if (dataPromise === null) {
                if (data.length > 0) {
                    filterData = data;
                }
                return;
            }
            data = await dataPromise;
            filterData = data;
        } catch (error) {
            console.error("Failed to fetch data:", error);
        }
    });

	function filterItems(event: Event) {
		const target = event.target as HTMLInputElement;
		const value = target.value.toLowerCase();
		filterData = data.filter(item => item.toLowerCase().includes(value));
	}

	function toggleCheckBox(id: string) {
		const checkbox = document.getElementById(id) as HTMLInputElement;
		if (checkbox) {
			checkbox.checked = !checkbox.checked;
		}
	}

	function itemClicked(item: string) {
        const searchBoxText = document.getElementById("text") as HTMLInputElement;
		if (!chosenItems.includes(item)) {
            if (maxItems === 1) {
                chosenItems = [item];
                searchBoxText.value = item;
                showDropdown = false;
            } else if (chosenItems.length < maxItems) {
				chosenItems = [...chosenItems, item];
                if (maxItems === 1) {
                    searchBoxText.value = item;
                    showDropdown = false;

                }
			} else {
				toggleCheckBox(item);
			}
		} else {
            if (maxItems === 1) {
                chosenItems = [];
                showDropdown = false;
                searchBoxText.value = "";
            } else {
                chosenItems = chosenItems.filter(i => i !== item);
                toggleCheckBox(item);
            }
		}
	}

    function toggleDropdown() {
        console.log("toggleDropdown");
        showDropdown = !showDropdown;
    }

    export function reportValidity() {
        return true;
    }

    export function setErrorMessage(message: string) {
        console.log("Setting error message: ", message);
    }
    
    $: console.log("Data Given: ", data);

</script>


<div class="mt-4">
    {#if showLabel}
        <label for={Name} class="block text-gray-700">{Name} </label>
    {/if}
    <input type="text" placeholder={placeholder} id="text" class="mt-2 w-full rounded-md border px-4 py-2 focus:ring-1 focus:ring-blue-600 focus:outline-none " on:input={filterItems} on:click={toggleDropdown}>
    <div class="absolute hidden bg-white shadow-md rounded mt-1 w-48" class:hidden={!showDropdown}>
		{#each filterData as item}
			{#if maxItems > 1}
				<div class="flex items-center">
					<input type="checkbox" id={item} name={item} value={item} on:click={() => itemClicked(item)} class="ml-1 mr-2">
					<label for={item}>{item}</label>
				</div>
			{:else}
				<button type="button" class="block w-full text-left px-4 py-2 hover:bg-gray-200" on:click={() => itemClicked(item)}>{item}</button>
			{/if}
		{/each}
	</div>
</div>
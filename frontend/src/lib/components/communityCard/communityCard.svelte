<script lang="ts">
	import { goto } from "$app/navigation";

	export let name: string;
    export let id : number;
	export let isPublic: boolean;
	export let description: string;
	export let tags: string[];
	export let degrees: string[];
	export let totalMembers: number;



    // --- Navigation Logic ---
	const targetUrl = `/communities/${id}`; // Construct the target URL

    function handleCardClick() {
		goto(targetUrl); // Navigate using SvelteKit's goto
	}

	// Accessibility: Allow keyboard navigation (Enter/Space)
	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault(); // Prevent space from scrolling page
			handleCardClick();
		}
	}

</script>

<!--
  Main container: Adopting style from the reference card.
  - w-full: Takes full width of its parent.
  - min-h-80: Ensures a minimum height.
  - flex flex-col: To enable flex-grow for content and mt-auto for footer.
-->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
	class="flex w-full flex-col space-y-4 rounded-lg border border-gray-200 bg-white p-4 min-h-80"
    on:click={handleCardClick}
	on:keydown={handleKeyDown}
>
	<!-- Header: Simplified -->
	<div class="flex items-center justify-between">
		<h2 class="truncate text-xl font-bold text-gray-900">
			{name}
		</h2>
		<!-- Status Badge - keeping its original styling as it's unique -->
		<span
			class="ml-3 flex-shrink-0 rounded-full px-3 py-1 text-sm font-medium
      {isPublic ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}"
		>
			{isPublic ? 'Public' : 'Private'}
		</span>
		<!-- Join button removed to match simpler header of reference card -->
	</div>

    <!-- Content Area: This will grow to push the bottom row down -->
    <div class="flex-grow space-y-3">
        <!-- Description: Using a slightly more prominent text for general description -->
        <div>
            <p class="mb-1 text-sm font-medium text-gray-500">Description</p>
            <p class="text-sm text-gray-700">{description}</p>
            <!--
                Alternative styling for description data if you want it like other fields:
                <p class="font-semibold text-gray-800">{description}</p>
            -->
        </div>

        <!-- Tags -->
        {#if tags && tags.length > 0}
            <div>
                <p class="mb-1 text-sm font-medium text-gray-500">Tags</p>
                <div class="flex flex-wrap gap-2">
                    {#each tags as tag}
                        <span
                            class="rounded-md bg-gray-100 px-2.5 py-0.5 text-sm font-semibold text-gray-800"
                        >
                            {tag}
                        </span>
                    {/each}
                </div>
            </div>
        {/if}

        <!-- Degrees -->
        {#if degrees && degrees.length > 0}
            <div>
                <p class="mb-1 text-sm font-medium text-gray-500">Relevant Degrees</p>
                <div class="flex flex-wrap gap-2">
                    {#each degrees as degree}
                        <span
                            class="rounded-md bg-gray-100 px-2.5 py-0.5 text-sm font-semibold text-gray-800"
                        >
                            {degree}
                        </span>
                    {/each}
                </div>
            </div>
        {/if}
    </div>


	<!-- Bottom Row: Simplified, no top border, pushed to bottom -->
	<div class="mt-auto flex items-center justify-between pt-2 text-sm text-gray-600">
		<div class="flex items-center space-x-2">
			<!-- Total members bold like "Year X" in reference -->
			<span class="text-base font-bold text-gray-900">{totalMembers}</span>
			<span class="text-gray-500">Members</span>
		</div>
	</div>
</div>
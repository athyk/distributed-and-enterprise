<script lang="ts">
    import { writable } from 'svelte/store';

    // Sample filter data
    const categories = writable([
        { name: "Chess", count: 120 },
        { name: "Clothing", count: 80 },
        { name: "Home & Kitchen", count: 45 },
        { name: "Beauty", count: 60 },
        { name: "Cars", count: 90 },
        { name: "Sports", count: 100 },
        { name: "Electronics", count: 150 },
        { name: "Books", count: 70 },
        { name: "Toys", count: 55 },
        { name: "Music", count: 110 },
        { name: "Health & Fitness", count: 65 }
    ]);

    const communityPub = writable([
        { name: "Public", count: 30 },
        { name: "Private", count: 40 }
    ]);

    const communityTags = writable([
        { name: "Homophobia", count: 100 },
        { name: "Racism", count: 60 },
        { name: "Xenophobia", count: 30 },
        { name: "Antisemitic", count: 30 },
        { name: "Misogyny", count: 50 },
        { name: "Ableism", count: 20 },
        { name: "Ageism", count: 40 },
        { name: "Hate Speech", count: 70 },
        { name: "Transphobia", count: 90 },
        { name: "Islamophobia", count: 80 }
    ]);

    const communityDegree = writable([
        { name: "Computer Science", count: 150 },
        { name: "Mathematics", count: 120 },
        { name: "Physics", count: 80 },
        { name: "Biology", count: 60 },
        { name: "Chemistry", count: 40 },
        { name: "Engineering", count: 100 },
        { name: "Economics", count: 70 },
        { name: "Psychology", count: 50 },
        { name: "Literature", count: 30 },
        { name: "Sociology", count: 20 }
    ]);

    let selectedCategories: Set<string> = new Set();
    let selectedCommunityPub: Set<string> = new Set();
    let selectedCommunityTags: Set<string> = new Set();
    let selectedCommunityDegree: Set<string> = new Set();

    let priceRange = [10, 500];

    const toggleFilter = (set: Set<string>, item: string) => {
        if (set.has(item)) set.delete(item);
        else set.add(item);
    };

    const clearFilters = () => {
        selectedCategories.clear();
        selectedCommunityPub.clear();
        selectedCommunityTags.clear();
        selectedCommunityDegree.clear();
        priceRange = [10, 500];
    };

    let expanded: Record<"categories" | "communityPub" | "communityTags" | "communityDegree" | "price", boolean> = {
        categories: true,
        communityPub: true,
        communityTags: true,
        communityDegree: true,
        price: true
    };

    const toggleSection = (section: keyof typeof expanded) => {
        expanded[section] = !expanded[section];
    };
</script>

<div class="w-72 bg-gray-900 text-white p-4  shadow-lg hidden lg:block">
    <!-- Categories -->
    <div class="border-b border-gray-700 py-2">
        <div class="flex justify-between items-center cursor-pointer p-2 hover:text-yellow-400" on:click={() => toggleSection('categories')}>
            Categories <span>{expanded.categories ? "▲" : "▼"}</span>
        </div>
        {#if expanded.categories}
            {#each $categories as category}
                <label class="flex items-center gap-2 p-2 cursor-pointer hover:bg-gray-800 ">
                    <input type="checkbox" class="accent-yellow-400" on:change={() => toggleFilter(selectedCategories, category.name)}>
                    {category.name} <span class="ml-auto text-gray-400">({category.count})</span>
                </label>
            {/each}
        {/if}
    </div>

    <!-- Community Type (Public/Private) -->
    <div class="border-b border-gray-700 py-2">
        <div class="flex justify-between items-center cursor-pointer p-2 hover:text-yellow-400" on:click={() => toggleSection('communityPub')}>
            Community Type <span>{expanded.communityPub ? "▲" : "▼"}</span>
        </div>
        {#if expanded.communityPub}
            {#each $communityPub as pub}
                <label class="flex items-center gap-2 p-2 cursor-pointer hover:bg-gray-800 rounded">
                    <input type="checkbox" class="accent-yellow-400" on:change={() => toggleFilter(selectedCommunityPub, pub.name)}>
                    {pub.name} <span class="ml-auto text-gray-400">({pub.count})</span>
                </label>
            {/each}
        {/if}
    </div>

    <!-- Community Tags (e.g., Racism, Homophobia) -->
    <div class="border-b border-gray-700 py-2">
        <div class="flex justify-between items-center cursor-pointer p-2 hover:text-yellow-400" on:click={() => toggleSection('communityTags')}>
            Community Tags <span>{expanded.communityTags ? "▲" : "▼"}</span>
        </div>
        {#if expanded.communityTags}
            {#each $communityTags as tag}
                <label class="flex items-center gap-2 p-2 cursor-pointer hover:bg-gray-800 rounded">
                    <input type="checkbox" class="accent-yellow-400" on:change={() => toggleFilter(selectedCommunityTags, tag.name)}>
                    {tag.name} <span class="ml-auto text-gray-400">({tag.count})</span>
                </label>
            {/each}
        {/if}
    </div>

    <!-- Community Degree (e.g., Computer Science, Engineering) -->
    <div class="border-b border-gray-700 py-2">
        <div class="flex justify-between items-center cursor-pointer p-2 hover:text-yellow-400" on:click={() => toggleSection('communityDegree')}>
            Community Degree <span>{expanded.communityDegree ? "▲" : "▼"}</span>
        </div>
        {#if expanded.communityDegree}
            {#each $communityDegree as degree}
                <label class="flex items-center gap-2 p-2 cursor-pointer hover:bg-gray-800 rounded">
                    <input type="checkbox" class="accent-yellow-400" on:change={() => toggleFilter(selectedCommunityDegree, degree.name)}>
                    {degree.name} <span class="ml-auto text-gray-400">({degree.count})</span>
                </label>
            {/each}
        {/if}
    </div>

    <!-- Price Range -->
    <div class="border-b border-gray-700 py-2">
        <div class="flex justify-between items-center cursor-pointer p-2 hover:text-yellow-400" on:click={() => toggleSection('price')}>
            Price Range <span>{expanded.price ? "▲" : "▼"}</span>
        </div>
        {#if expanded.price}
            <div class="flex flex-col px-2">
                <input type="range" min="10" max="1000" step="10" bind:value={priceRange[0]} class="accent-yellow-400">
                <input type="range" min="10" max="1000" step="10" bind:value={priceRange[1]} class="accent-yellow-400">
                <div class="text-center text-gray-400">£{priceRange[0]} - £{priceRange[1]}</div>
            </div>
        {/if}
    </div>

    <!-- Joke Section (For Mates) -->
    <div class="mt-4 text-center text-gray-400">
        <p class="italic">"Why don't skeletons fight each other? They don't have the guts!"</p>
    </div>

    <!-- Clear Filters Button -->
    <button class="w-full bg-red-600 hover:bg-red-700 text-white py-2 mt-4 rounded-lg transition duration-300" on:click={clearFilters}>
        Clear All Filters
    </button>
</div>

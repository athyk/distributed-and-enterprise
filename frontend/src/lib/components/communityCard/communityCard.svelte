<script lang="ts">
  export let name: string;
  export let isPublic: boolean; 
  export let description: string;
  export let tags: string[];
  export let degrees: string[];
  export let totalMembers: number;
  export let creationDate: string;
</script>

<div class="max-w-2xl mx-auto p-6 bg-white dark:bg-gray-900 rounded-xl shadow-lg space-y-4">
  <!-- Header with Title and Status -->
  <div class="flex flex-col md:flex-row items-center justify-between border-b pb-4">
    <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
      {name}
    </h2>
    <div class="flex items-center space-x-4 mt-4 md:mt-0">
      <!-- Status Badge -->
      <span class="px-3 py-1 rounded-full text-sm font-medium
        {isPublic ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
        {isPublic ? "Public" : "Private"}
      </span>
      <!-- Join Button -->
      <button class="bg-blue-600 text-white px-4 py-2 rounded font-semibold hover:bg-blue-700 transition">
        Join Community +
      </button>
    </div>
  </div>

  <!-- Description -->
  <p class="text-gray-700 dark:text-gray-300">
    {description}
  </p>

  <!-- Tags -->
  {#if tags && tags.length > 0}
    <div class="flex flex-wrap gap-2">
      {#each tags as tag}
        <span class="bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-200 px-3 py-1 rounded-full text-sm">
          {tag}
        </span>
      {/each}
    </div>
  {/if}

  <!-- Degrees -->
  {#if degrees && degrees.length > 0}
    <div class="flex flex-wrap gap-2">
      {#each degrees as degree}
        <span class="bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-200 px-3 py-1 rounded-full text-sm">
          {degree}
        </span>
      {/each}
    </div>
  {/if}

  <!-- Bottom Row: Total Members & Creation Date -->
  <div class="flex items-center justify-between text-gray-600 dark:text-gray-400 border-t pt-4">
    <div class="flex items-center space-x-2">
      <span class="text-lg font-bold text-gray-900 dark:text-white">{totalMembers}</span>
      <span class="text-sm">Members</span>
    </div>
    <div class="text-sm">
      {creationDate}
    </div>
  </div>
</div>

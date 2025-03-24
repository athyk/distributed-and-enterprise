<script lang="ts">
  export let title: string = "Announcement Title";
  export let description: string = "Announcement Description";
  export let location: string = "Location";
  export let datetime: string = "2025-01-01";
  export let duration: number = 1;
  export let tags: number[] = [1, 2];
</script>

<div class="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg shadow-md w-full max-w-2xl">
  <!-- Title Section -->
  <div class="flex justify-between items-center mb-2">
    <h1 class="text-xl font-bold text-gray-900 dark:text-white">
      {title}
    </h1>
  </div>
  
  <!-- Location, Date and Duration Section -->
  <div class="flex justify-between items-center mb-2">
    <p class="text-lg font-semibold text-gray-900 dark:text-white">
      {location}
    </p>
    <p class="text-lg font-semibold text-gray-900 dark:text-white">
      {datetime} | {duration} hr{duration > 1 ? 's' : ''}
    </p>
  </div>
  
  <!-- Description -->
  <p class="text-sm text-gray-700 dark:text-gray-300">
    {description}
  </p>
  
  <!-- Tags -->
  <div class="mt-3 flex flex-wrap gap-2">
    {#each tags as tag}
      <span class="text-sm bg-gray-300 dark:bg-gray-600 px-2 py-1 rounded">
        Tag {tag}
      </span>
    {/each}
  </div>
</div>

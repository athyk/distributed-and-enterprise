<script lang="ts">
    export let name: string = "Tech Innovators Hub";
    export let description: string =
      "Join a vibrant community of developers, designers, and tech enthusiasts. Collaborate on projects, share insights, and drive innovation in the tech industry.";
    export let tags: string[] = ["JavaScript", "Svelte", "React", "Tailwind", "Node.js"];
    export let degrees: string[] = ["Beginner", "Intermediate", "Expert"];
    export let totalMembers: string = "3,425";
    export let creationDate: string = "February 2021";
    export let isPublic: boolean = true;
  </script>
  

<div class="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg shadow-md w-full max-w-2xl">
  <div class="flex justify-between items-center mb-2">
    <h2 class="text-lg font-semibold text-gray-900 dark:text-white">{name}</h2>
    <span class="text-sm px-2 py-1 rounded-md bg-gray-200 dark:bg-gray-700">
      {isPublic ? "Public" : "Private"}
    </span>
  </div>

  <p class="text-sm text-gray-700 dark:text-gray-300">{description}</p>

  <div class="mt-3 flex flex-wrap gap-2">
    {#each tags as tag}
      <span class="text-sm bg-gray-300 dark:bg-gray-600 px-2 py-1 rounded">{tag}</span>
    {/each}
  </div>

  <div class="mt-2 flex flex-wrap gap-2">
    {#each degrees as degree}
      <span class="text-sm bg-gray-400 dark:bg-gray-500 px-2 py-1 rounded">{degree}</span>
    {/each}
  </div>

  <div class="mt-4 text-sm text-gray-600 dark:text-gray-400">
    <p>Total Members: {totalMembers}</p>
    <p>{creationDate}</p>
  </div>

  <div class="mt-4 flex justify-end">
    <button class="px-4 py-2 text-md rounded bg-blue-600 text-white hover:bg-blue-700">
      {isPublic ? "Join Community +" : "Request Access +"}
    </button>
  </div>
</div>

<script lang="ts">
    export let postedName: string = "Your Mum";
    export let communityHeader: string = "Jake special group";
    export let community: string = "Talking to girls";

    export let description: string =
      "Join a vibrant community of developers, designers, and tech enthusiasts. Collaborate on projects, share insights, and drive innovation in the tech industry.";
    export let tags: string[] = ["JavaScript", "Svelte", "React", "Tailwind", "Node.js"];

    export let creationDate: string = "February 2021";

  </script>
  



 
  <div class="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg shadow-md w-full max-w-2xl">
    <div class="flex justify-between items-center mb-2">
      <h1 class="text-xl font-bold text-gray-900 dark:text-white">
        {communityHeader}
      </h1>
    </div>
  
    <div class="flex justify-between items-center mb-2">
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white">
        Posted By: {postedName}
      </h2>
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white">
        Community: {community}
      </h2>
    </div>
  
    <p class="text-sm text-gray-700 dark:text-gray-300">{description}</p>
  
    <div class="mt-3 flex justify-between items-center">
      <div class="flex flex-wrap gap-2">
        {#each tags as tag}
        <span class="text-sm bg-gray-300 dark:bg-gray-600 px-2 py-1 rounded">
          {tag}
        </span>
        {/each}
      </div>
      <p class="text-sm text-gray-500 dark:text-gray-400">{creationDate}</p>
    </div>
  </div>
  

  
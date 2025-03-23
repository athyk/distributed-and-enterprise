<script lang="ts">
  // Define properties for the profile section.
  export let profileImage: string;
  export let profileName: string;
  
  // Define an array of community info objects.
  export let communitiesInfo: { 
    id: number; 
    name: string; 
    imageUrl?: string;
  }[];
</script>

<aside class="w-full max-w-xs bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 space-y-6 h-screen flex flex-col">
  <!-- Profile Section -->
  

  <!-- Communities Info List -->
  <div class="space-y-4 flex-1 overflow-y-auto">
    {#each communitiesInfo as community (community.id)}
      <div class="flex items-center p-2 bg-gray-100 dark:bg-gray-700 rounded-md">
        <img 
          src={community.imageUrl || "https://via.placeholder.com/40"} 
          alt={community.name} 
          class="w-10 h-10 rounded-full object-cover"
        />
        <span class="ml-3 text-sm font-medium text-gray-900 dark:text-gray-100">
          {community.name}
        </span>
      </div>
    {/each}
  </div>

  <!-- Bottom Section: Sign Out Button -->
  <div>
    <button class="w-full bg-red-500 text-white py-2 rounded hover:bg-red-600 transition">
      Sign Out
    </button>
  </div>
</aside>

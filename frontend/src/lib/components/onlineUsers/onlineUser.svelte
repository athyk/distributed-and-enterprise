<script lang="ts">
  import { goto } from '$app/navigation';

  // Define properties for the profile section.
  export let userInfo: { 
    id: number; 
    name: string; 
    imageUrl?: string;
    isOnline?: boolean;
  }[];

  // Sort users by online status (online users first)
  $: sortedUserInfo = [...userInfo].sort((a, b) => (b.isOnline ? 1 : 0) - (a.isOnline ? 1 : 0));

  function goToSettings() {
    goto('/settings'); // Update the path as needed
  }
</script>

<aside class="w-full max-w-xs bg-white dark:bg-gray-800 shadow-lg p-6 h-screen flex flex-col">
  <!-- Users List (Scrollable) -->
  <div class="space-y-4 flex-1 overflow-y-auto">
    {#each sortedUserInfo as user (user.id)}
      <div class="flex items-center p-2 bg-gray-100 dark:bg-gray-700 rounded-md relative">
        <div class="relative">
          <img 
            src={user.imageUrl || "https://via.placeholder.com/40"} 
            alt={user.name} 
            class="w-10 h-10 rounded-full object-cover"
          />
          {#if user.isOnline}
            <span class="absolute bottom-0 right-0 block w-3 h-3 bg-green-500 border-2 border-white dark:border-gray-800 rounded-full"></span>
          {:else}
            <span class="absolute bottom-0 right-0 block w-3 h-3 bg-gray-500 border-2 border-white dark:border-gray-800 rounded-full"></span>
          {/if}
        </div>
        <span class="ml-3 text-sm font-medium text-gray-900 dark:text-gray-100">
          {user.name}
        </span>
      </div>
    {/each}
  </div>

  <!-- Settings Button -->
  <button 
    on:click={goToSettings}
    class="mt-4 w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
    ⚙️ Settings
  </button>
</aside>

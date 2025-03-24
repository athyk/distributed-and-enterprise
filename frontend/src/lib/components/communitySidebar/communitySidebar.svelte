<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { goto } from '$app/navigation'; // Import goto for navigation

  export let communitiesInfo: { id: number; name: string; imageUrl: string }[];

  const dispatch = createEventDispatcher();

  function selectCommunity(id: number) {
    dispatch("selectCommunity", id);
  }

  function createCommunity() {
    goto('communities/create'); // Redirects to /create page
  }
</script>

<ul class="bg-gray-800 text-white h-full p-4 space-y-2">
  {#each communitiesInfo as community}
    <li 
      on:click={() => selectCommunity(community.id)} 
      class="cursor-pointer hover:bg-gray-600 p-2 rounded flex items-center space-x-3">
      <img src={community.imageUrl} alt={community.name} class="w-10 h-10 rounded-full" />
      <span>{community.name}</span>
    </li>
  {/each}

  <!-- Create Community Button -->
  <button 
    on:click={createCommunity} 
    class="mt-4 w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
    + Create Community
  </button>
</ul>

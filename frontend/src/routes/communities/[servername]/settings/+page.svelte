<script lang="ts">
    export let activeTab: string;
  </script>
  
  <div class="flex-1 p-6">
    {#if activeTab === "General"}
      <h1 class="text-3xl font-bold">General Settings</h1>
      <p>Manage general settings for your communities.</p>
    {:else if activeTab === "Update"}
      <h1 class="text-3xl font-bold">Update Community</h1>
      <p>Modify details for your community.</p>
    {:else if activeTab === "Delete"}
      <h1 class="text-3xl font-bold">Delete Community</h1>
      <p>Are you sure you want to delete this community?</p>
    {:else if activeTab === "Permissions"}
      <h1 class="text-3xl font-bold">Permissions</h1>
      <p>Manage roles and access levels.</p>
    {/if}
  </div>
  
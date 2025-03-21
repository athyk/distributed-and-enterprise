<script lang="ts">
  let searchQuery: string = ""; // Explicitly typed for TypeScript

  function search(): void {
      console.log("Searching for:", searchQuery);
  }

  function create(): void {
      console.log("Create button clicked");
  }

  function remove(): void {
      console.log("Remove button clicked");
  }

  function update(): void {
      console.log("Update button clicked");
  }

  function deleteItem(): void {
      console.log("Delete button clicked");
  }
</script>

<div class="min-h-screen flex flex-col items-center text-gray-900 px-6 sm:px-12 py-12">

  <!-- Hero Section -->
  <header class="text-center mb-10">
      <h1 class="text-4xl sm:text-5xl font-bold">Manage Your Communities</h1>
      <p class="text-lg text-gray-600 mt-2">
          Search, create, update, or remove communities with ease.
      </p>
  </header>

  <!-- Search Bar -->
  <div class="w-full max-w-lg flex items-center gap-2 border border-gray-300 p-3 rounded-full shadow-sm">
      <input 
          type="text" 
          bind:value={searchQuery} 
          placeholder="Search for a community..." 
          class="w-full text-gray-900 outline-none px-4 bg-transparent"
      />
      <button 
          on:click={search} 
          class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-full shadow-md transition">
          Search
      </button>
  </div>

<!-- Button Group -->
<div class="flex flex-wrap gap-4 justify-center mt-10">
  <button on:click={create} class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-full shadow-md transition">
      Create
  </button>
  <button on:click={update} class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-full shadow-md transition">
      Update
  </button>
  <button on:click={remove} class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-full shadow-md transition">
      Remove
  </button>
  <button on:click={deleteItem} class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-full shadow-md transition">
      Delete
  </button>
</div>

</div>

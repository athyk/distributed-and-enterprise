<script lang="ts">
  let activeTab: string = "update";

  // Form data
  let formData = {
    name: "",
    description: "",
    public: false,
    tags: [] as Number[],
    degrees: [] as string[],
  };

  // Function to toggle public status
  function togglePublic() {
    formData.public = !formData.public;
  }

  // Function to add a new tag
  function addTag() {
    const newTag = prompt("Enter a new tag:");
    if (newTag) formData.tags = [...formData.tags, newTag];
  }

  // Function to remove a tag
  function removeTag(index: number) {
    formData.tags = formData.tags.filter((_, i) => i !== index);
  }

  // Function to add a new degree
  function addDegree() {
    const newDegree = prompt("Enter a new degree:");
    if (newDegree) formData.degrees = [...formData.degrees, newDegree];
  }

  // Function to remove a degree
  function removeDegree(index: number) {
    formData.degrees = formData.degrees.filter((_, i) => i !== index);
  }

  // Function to update the community (PUT request)
// Extract the community ID from the URL
const communityId = window.location.pathname.split('/')[2];

async function updateCommunity() {
  console.log("Updating community with data:", formData);
  
  try {
    let response = await fetch(`http://localhost:8000/community/${communityId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });
    
    if (!response.ok) {
      throw new Error("Failed to update community");
    }
    
    let data = await response.json();
    console.log(data.id);
  } catch (error) {
    console.error("Error updating community:", error);
  }
}

async function deleteCommunity() {
  console.log("Deleting community...");
  
  try {
    let response = await fetch(`http://localhost:8000/community/${communityId}`, {
      method: "DELETE",
    });
    
    if (!response.ok) {
      throw new Error("Failed to delete community");
    }
    
    console.log("Community deleted successfully");
  } catch (error) {
    console.error("Error deleting community:", error);
  }
}

</script>

<!-- Main container -->
<div class="flex min-h-screen bg-gray-100 dark:bg-gray-900">
  <!-- Sidebar -->
  <aside class="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 p-4">
    <h2 class="text-lg font-bold mb-4 text-gray-900 dark:text-gray-100">
      Community Settings
    </h2>
    <nav class="space-y-2">
      <button
        on:click={() => (activeTab = "update")}
        class="w-full text-left px-3 py-2 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 transition focus:outline-none text-gray-800 dark:text-gray-200 {activeTab === 'update' ? 'bg-gray-200 dark:bg-gray-700 font-semibold' : ''}"
      >
        Update Community
      </button>
      <button
        on:click={() => (activeTab = "delete")}
        class="w-full text-left px-3 py-2 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 transition focus:outline-none text-gray-800 dark:text-gray-200 {activeTab === 'delete' ? 'bg-gray-200 dark:bg-gray-700 font-semibold' : ''}"
      >
        Delete Community
      </button>
    </nav>
  </aside>

  <!-- Content Area -->
  <main class="flex-1 p-8">
    {#if activeTab === "update"}
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
        Update Community
      </h1>

      <div class="bg-white dark:bg-gray-800 rounded-md p-4 shadow">
        <!-- Name -->
        <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Name</label>
        <input
          id="name"
          type="text"
          bind:value={formData.name}
          class="block w-full mt-1 mb-3 rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-gray-200"
        />

        <!-- Description -->
        <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Description</label>
        <textarea
          id="description"
          bind:value={formData.description}
          class="block w-full mt-1 mb-3 rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-gray-200"
        ></textarea>

        <!-- Public Toggle -->
        <div class="flex items-center mb-3">
          <input id="public" type="checkbox" bind:checked={formData.public} class="mr-2" />
          <label for="public" class="text-sm font-medium text-gray-700 dark:text-gray-300">Public</label>
        </div>

        <!-- Tags -->
        <div class="mb-3">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Tags</label>
          {#each formData.tags as tag, i}
            <div class="flex items-center mt-1">
              <span class="bg-gray-300 dark:bg-gray-700 text-gray-900 dark:text-gray-100 px-2 py-1 rounded mr-2">{tag}</span>
              <button on:click={() => removeTag(i)} class="text-red-500 hover:text-red-700">×</button>
            </div>
          {/each}
          <button on:click={addTag} class="mt-2 text-blue-600 hover:text-blue-800 text-sm">+ Add Tag</button>
        </div>

        <!-- Degrees -->
        <div class="mb-3">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Degrees</label>
          {#each formData.degrees as degree, i}
            <div class="flex items-center mt-1">
              <span class="bg-gray-300 dark:bg-gray-700 text-gray-900 dark:text-gray-100 px-2 py-1 rounded mr-2">{degree}</span>
              <button on:click={() => removeDegree(i)} class="text-red-500 hover:text-red-700">×</button>
            </div>
          {/each}
          <button on:click={addDegree} class="mt-2 text-blue-600 hover:text-blue-800 text-sm">+ Add Degree</button>
        </div>

        <button on:click={updateCommunity} class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">
          Update Community
        </button>
      </div>

    {:else if activeTab === "delete"}
      <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
        Delete Community
      </h1>
      <p class="text-gray-700 dark:text-gray-300 mb-4">
        Permanently delete this community. This action cannot be undone.
      </p>
      <button on:click={deleteCommunity} class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition">
        Delete Community
      </button>
    {/if}
  </main>
</div>

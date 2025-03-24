<script lang="ts">
    // Data model for the form
    let formData = {
      name: "",
      description: "",
      public: false,
      tags: [] as string[],
      degrees: [] as string[]
    };
  
    // Function to handle adding a tag
    function addTag() {
      const newTag = prompt("Enter a new tag");
      if (newTag) formData.tags = [...formData.tags, newTag];
    }
  
    // Function to handle removing a tag
    function removeTag(index: number) {
      formData.tags.splice(index, 1);
      formData.tags = [...formData.tags];
    }
  
    // Function to handle adding a degree
    function addDegree() {
      const newDegree = prompt("Enter a new degree");
      if (newDegree) formData.degrees = [...formData.degrees, newDegree];
    }
  
    // Function to handle removing a degree
    function removeDegree(index: number) {
      formData.degrees.splice(index, 1);
      formData.degrees = [...formData.degrees];
    }
  
    // Function to handle form submission
    function createCommunity() {
      console.log("Creating community with data:", formData);
      // Add your API call or store logic here
    }
  </script>
  
  <!-- Container -->
  <div class="p-6 max-w-xl mx-auto bg-gray-900 text-white rounded-md shadow-md">
    <h1 class="text-2xl font-bold mb-4">Create Community</h1>
    
    <!-- Name Field -->
    <div class="mb-4">
      <label for="communityName" class="block text-sm font-medium mb-1">Name</label>
      <input
        id="communityName"
        type="text"
        bind:value={formData.name}
        class="w-full rounded-md bg-gray-800 border border-gray-700 focus:border-blue-500 focus:ring-blue-500 p-2"
      />
    </div>
  
    <!-- Description Field -->
    <div class="mb-4">
      <label for="description" class="block text-sm font-medium mb-1">Description</label>
      <textarea
        id="description"
        rows="3"
        bind:value={formData.description}
        class="w-full rounded-md bg-gray-800 border border-gray-700 focus:border-blue-500 focus:ring-blue-500 p-2"
      ></textarea>
    </div>
  
    <!-- Public Checkbox -->
    <div class="mb-4 flex items-center">
      <input
        id="publicCheckbox"
        type="checkbox"
        bind:checked={formData.public}
        class="mr-2"
      />
      <label for="publicCheckbox" class="text-sm">Public</label>
    </div>
  
    <!-- Tags -->
    <div class="mb-4">
      <label class="block text-sm font-medium mb-1">Tags</label>
      <div class="flex flex-wrap gap-2">
        {#each formData.tags as tag, index}
          <span class="bg-gray-800 border border-gray-700 px-2 py-1 rounded-md flex items-center">
            {tag}
            <button
              type="button"
              class="ml-2 text-red-400 hover:text-red-600"
              on:click={() => removeTag(index)}
            >
              &times;
            </button>
          </span>
        {/each}
      </div>
      <button
        type="button"
        class="text-blue-400 hover:text-blue-600 mt-1 text-sm"
        on:click={addTag}
      >
        + Add Tag
      </button>
    </div>
  
    <!-- Degrees -->
    <div class="mb-4">
      <label class="block text-sm font-medium mb-1">Degrees</label>
      <div class="flex flex-wrap gap-2">
        {#each formData.degrees as degree, index}
          <span class="bg-gray-800 border border-gray-700 px-2 py-1 rounded-md flex items-center">
            {degree}
            <button
              type="button"
              class="ml-2 text-red-400 hover:text-red-600"
              on:click={() => removeDegree(index)}
            >
              &times;
            </button>
          </span>
        {/each}
      </div>
      <button
        type="button"
        class="text-blue-400 hover:text-blue-600 mt-1 text-sm"
        on:click={addDegree}
      >
        + Add Degree
      </button>
    </div>
  
    <!-- Create Button -->
    <button
      on:click={createCommunity}
      class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-md"
    >
      Create Community
    </button>
  </div>
  
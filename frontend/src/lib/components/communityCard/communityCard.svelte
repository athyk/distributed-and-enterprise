<div class="max-w-md mx-auto p-6 bg-white dark:bg-gray-900 rounded-xl shadow-lg">
  <!-- Title -->
  <h2 class="text-2xl font-semibold text-gray-900 dark:text-white text-center mb-6">
    Create Communities
  </h2>

  <!-- Community Name Input -->
  <input 
    type="text" 
    placeholder="Community Name"
    class="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none"
  />

  <!-- Community Publicity -->
  <div class="relative mt-4">
    <select 
      class="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white appearance-none focus:ring-2 focus:ring-blue-500"
    >
      <option>Community Publicity</option>
    </select>
  </div>

  <!-- Community Tags -->
  <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300 mt-6 mb-2">Community Tags</h3>
  
  <!-- Tags Container -->
  <div id="tags-container" class="flex flex-wrap gap-2 mb-3"></div>

  <!-- Tag Input Field -->
  <input 
    id="tag-input"
    type="text" 
    placeholder="Type #tag and press Enter"
    class="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none"
  />

  <!-- Community Degrees -->
  <div class="relative mt-6">
    <select 
      class="w-full p-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white appearance-none focus:ring-2 focus:ring-blue-500"
    >
      <option>Community Degrees</option>
    </select>
  </div>

  <!-- Submit Button -->
  <button 
    class="mt-6 w-full bg-blue-600 text-white p-3 rounded-lg font-semibold hover:bg-blue-700 transition"
  >
    Submit
  </button>
</div>
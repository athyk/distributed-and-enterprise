<script lang="ts">
    export let name: string = "Max Haley";
    export let imageUrl: string = "https://randomuser.me/api/portraits/men/75.jpg";
    export let imageSize: string = "w-16 h-16"; // e.g. "w-16 h-16", "w-20 h-20", etc.
    export let containerClass: string = ""; // Additional classes for the container
    export let textClass: string = ""; // Additional classes for the text
  </script>
  
  <div class={`flex items-center p-3 bg-white dark:bg-gray-800 rounded-lg ${containerClass}`}>
    <img
      src={imageUrl}
      alt={name}
      class={`${imageSize} rounded-full object-cover`}
    />
    <p class={`ml-4 text-lg font-semibold text-gray-900 dark:text-gray-100 ${textClass}`}>
      {name}
    </p>
  </div>
  
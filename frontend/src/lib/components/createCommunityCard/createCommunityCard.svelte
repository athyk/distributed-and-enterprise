<script lang="ts">
    export let eventTitle: string = "Event Title";
    export let description: string =
      "Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc Event Desc";
    export let hostedBy: string = "Hosted by X Community";
    export let eventDate: string = "Event Date";
    export let eventTags: string = "Event Tags";
    export let eventTime: string = "Event Time Duration";
    export let eventLocation: string = "Event Location";
    export let attendees: string = "Number of Attendees";
  </script>
  
  <div class="bg-white dark:bg-gray-900 p-6 rounded-2xl shadow-lg w-full max-w-2xl mx-auto">
    <!-- Event Title -->
    <h1 class="text-2xl font-bold text-center text-gray-900 dark:text-white mb-4">
      {eventTitle}
    </h1>
  
    <!-- Event Description -->
    <p class="text-sm text-gray-700 dark:text-gray-300 text-center leading-relaxed mb-6">
      {description}
    </p>
  
    <!-- Event Details Section -->
  <!-- Event Details Section -->
  <div class="bg-gradient-to-r from-gray-100 to-gray-300 dark:from-gray-800 dark:to-gray-900 p-6 rounded-2xl grid grid-cols-2 gap-6 text-gray-900 dark:text-white shadow-lg">
    <div class="flex items-center gap-3">
      <span class="text-lg">📍</span>
      <span class="font-semibold">{hostedBy}</span>
    </div>
    
    <div class="flex items-center gap-3">
      <span class="text-lg">📅</span>
      <span class="font-semibold">{eventDate}</span>
    </div>
  
    <div class="flex items-center gap-3">
      <span class="text-lg">🏷️</span>
      <span class="text-gray-700 dark:text-gray-300">{eventTags}</span>
    </div>
  
    <div class="flex items-center gap-3">
      <span class="text-lg">⏳</span>
      <span class="text-gray-700 dark:text-gray-300">{eventTime}</span>
    </div>
  
    <div class="flex items-center gap-3">
      <span class="text-lg">📌</span>
      <span class="text-gray-700 dark:text-gray-300">{eventLocation}</span>
    </div>
  
    <div class="flex items-center gap-3">
      <span class="text-lg">👥</span>
      <span class="text-gray-700 dark:text-gray-300">{attendees}</span>
    </div>
  </div>
  
    <!-- Action Buttons -->
    <div class="mt-6 flex justify-between gap-4">
      <button class="w-1/2 py-3 rounded-xl bg-gray-300 dark:bg-gray-700 text-gray-900 dark:text-white font-medium transition-all hover:bg-gray-400 dark:hover:bg-gray-600">
        View Event
      </button>
      <button class="w-1/2 py-3 rounded-xl bg-blue-600 text-white font-medium transition-all hover:bg-blue-700">
        Sign Me Up
      </button>
    </div>
  </div>
  
<script lang="ts">
    export let username: string = "Hydralisk157";
    export let timestamp: string = "16/12/2024 13:11";
    export let messageText: string = "Go it, thanks man\n*Got it";
    export let avatarUrl: string = "https://via.placeholder.com/40";
  </script>
  
  <!-- Container for the message card -->
  <div class="flex items-start space-x-3 p-2">
    <!-- Avatar -->
    <img 
      class="w-10 h-10 rounded-full object-cover flex-shrink-0" 
      src={avatarUrl} 
      alt={username} 
    />
    
    <!-- Main message content -->
    <div class="flex flex-col">
      <!-- Username and timestamp row -->
      <div class="flex items-baseline space-x-2">
        <span class="font-semibold text-gray-900 dark:text-gray-100">
          {username}
        </span>
        <span class="text-xs text-gray-500 dark:text-gray-400">
          {timestamp}
        </span>
      </div>
    
      <!-- Message text -->
      <p class="text-gray-800 dark:text-gray-200 whitespace-pre-line mt-1">
        {messageText}
      </p>
    </div>
  </div>
  
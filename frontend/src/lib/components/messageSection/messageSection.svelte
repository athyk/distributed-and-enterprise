<script lang="ts">
  export let messages: { username: string; timestamp: string; messageText: string; avatarUrl: string }[];
</script>

<div class="p-4 bg-gray-900 text-white h-full overflow-auto">
  {#each messages as message}
    <div class="p-2 border-b border-gray-700 flex items-center space-x-3">
      <img src={message.avatarUrl} alt="Avatar" class="w-10 h-10 rounded-full" />
      <div>
        <span class="font-bold">{message.username}</span>
        <p>{message.messageText}</p>
        <small class="text-gray-400">{message.timestamp}</small>
      </div>
    </div>
  {/each}
</div>

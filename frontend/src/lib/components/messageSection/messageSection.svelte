<script lang="ts">
	export let messages: {
		username: string;
		timestamp: string;
		messageText: string;
		avatarUrl: string;
	}[];
</script>

<div class="h-full overflow-auto bg-gray-900 p-4 text-white">
	{#each messages as message}
		<div class="flex items-center space-x-3 border-b border-gray-700 p-2">
			<img src={message.avatarUrl} alt="Avatar" class="h-10 w-10 rounded-full" />
			<div>
				<span class="font-bold">{message.username}</span>
				<p>{message.messageText}</p>
				<small class="text-gray-400">{message.timestamp}</small>
			</div>
		</div>
	{/each}
</div>

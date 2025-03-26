<script lang="ts">
	import CommunitySidebar from '$components/communitySidebar/communitySidebar.svelte';
	import MessageSection from '$components/messageSection/MessageSection.svelte';
	import { goto } from '$app/navigation';

	interface Community {
		id: number;
		name: string;
		imageUrl: string;
	}

	interface Message {
		username: string;
		timestamp: string;
		messageText: string;
		avatarUrl: string;
	}

	let selectedCommunityId: number = 1;

	let communitiesInfo: Community[] = [
		{
			id: 1,
			name: 'Tech Innovators',
			imageUrl:
				'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=100&q=60'
		},
		{
			id: 2,
			name: 'Art Lovers',
			imageUrl:
				'https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?auto=format&fit=crop&w=100&q=60'
		},
		{
			id: 3,
			name: 'Gaming Gurus',
			imageUrl:
				'https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?auto=format&fit=crop&w=100&q=60'
		}
	];

	let communityMessages: Record<number, Message[]> = {
		1: [
			{
				username: 'User1',
				timestamp: '16/12/2024 12:59',
				messageText: 'AI is amazing!',
				avatarUrl: 'https://randomuser.me/api/portraits/men/55.jpg'
			},
			{
				username: 'User2',
				timestamp: '16/12/2024 13:05',
				messageText: 'Hello world!',
				avatarUrl: 'https://randomuser.me/api/portraits/women/45.jpg'
			}
		],
		2: [
			{
				username: 'ArtistA',
				timestamp: '16/12/2024 14:00',
				messageText: 'Check out my new painting!',
				avatarUrl: 'https://randomuser.me/api/portraits/men/32.jpg'
			}
		],
		3: [
			{
				username: 'Gamer1',
				timestamp: '16/12/2024 15:00',
				messageText: 'Anyone up for a game?',
				avatarUrl: 'https://randomuser.me/api/portraits/women/50.jpg'
			}
		]
	};

	function selectCommunity(id: number) {
		selectedCommunityId = id;
	}

	function goToSettings() {
		goto(`/communities/${selectedCommunityId}/settings`);
	}
</script>

<div class="flex h-screen">
	<!-- Sidebar -->
	<div class="w-64 flex-none">
		<CommunitySidebar {communitiesInfo} on:selectCommunity={(e) => selectCommunity(e.detail)} />
	</div>

	<!-- Main Content -->
	<div class="flex flex-1 flex-col">
		<MessageSection messages={communityMessages[selectedCommunityId] ?? []} />
	</div>

	<!-- Online Users Section -->
	<aside class="flex h-screen w-64 flex-col bg-white p-6 shadow-lg dark:bg-gray-800">
		<h3 class="mb-2 text-lg font-semibold text-gray-900 dark:text-gray-100">Online Users</h3>

		<!-- Settings Button -->
		<button
			on:click={goToSettings}
			class="mt-4 w-full rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-600"
		>
			⚙️ Settings
		</button>
	</aside>
</div>

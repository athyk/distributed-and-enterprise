<script lang="ts">
  import CommunitySidebar from '$components/communitySidebar/CommunitySidebar.svelte';
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

  interface User {
    id: number;
    name: string;
    imageUrl?: string;
    isOnline?: boolean;
  }

  let selectedCommunityId: number = 1;

  let communitiesInfo: Community[] = [
    { id: 1, name: "Tech Innovators", imageUrl: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=100&q=60" },
    { id: 2, name: "Art Lovers", imageUrl: "https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?auto=format&fit=crop&w=100&q=60" },
    { id: 3, name: "Gaming Gurus", imageUrl: "https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?auto=format&fit=crop&w=100&q=60" }
  ];

  let communityMessages: Record<number, Message[]> = {
    1: [
      { username: "User1", timestamp: "16/12/2024 12:59", messageText: "AI is amazing!", avatarUrl: "https://randomuser.me/api/portraits/men/55.jpg" },
      { username: "User2", timestamp: "16/12/2024 13:05", messageText: "Hello world!", avatarUrl: "https://randomuser.me/api/portraits/women/45.jpg" }
    ],
    2: [
      { username: "ArtistA", timestamp: "16/12/2024 14:00", messageText: "Check out my new painting!", avatarUrl: "https://randomuser.me/api/portraits/men/32.jpg" }
    ],
    3: [
      { username: "Gamer1", timestamp: "16/12/2024 15:00", messageText: "Anyone up for a game?", avatarUrl: "https://randomuser.me/api/portraits/women/50.jpg" }
    ]
  };

  let communityUsers: Record<number, User[]> = {
    1: [
      { id: 1, name: "John Doe", imageUrl: "https://randomuser.me/api/portraits/men/75.jpg", isOnline: true },
      { id: 2, name: "Jane Smith", imageUrl: "https://randomuser.me/api/portraits/women/65.jpg", isOnline: false }
    ],
    2: [
      { id: 3, name: "ArtistA", imageUrl: "https://randomuser.me/api/portraits/men/32.jpg", isOnline: true }
    ],
    3: [
      { id: 4, name: "Gamer1", imageUrl: "https://randomuser.me/api/portraits/women/50.jpg", isOnline: true }
    ]
  };

  function selectCommunity(id: number) {
    selectedCommunityId = id;
  }

  function goToSettings() {
    goto(`/communities/${selectedCommunityId}/settings`);
}


  // Sort users by online status (online first)
  $: sortedUsers = [...(communityUsers[selectedCommunityId] ?? [])].sort(
    (a, b) => (b.isOnline ? 1 : 0) - (a.isOnline ? 1 : 0)
  );
</script>

<div class="flex h-screen">
  <!-- Sidebar -->
  <div class="flex-none w-64">
    <CommunitySidebar {communitiesInfo} on:selectCommunity={e => selectCommunity(e.detail)} />
  </div>

  <!-- Main Content -->
  <div class="flex-1 flex flex-col">
    <MessageSection messages={communityMessages[selectedCommunityId] ?? []} />
  </div>

  <!-- Online Users Section -->
  <aside class="w-64 bg-white dark:bg-gray-800 shadow-lg p-6 h-screen flex flex-col">
    <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">Online Users</h3>

    <!-- Users List (Scrollable) -->
    <div class="space-y-4 flex-1 overflow-y-auto">
      {#each sortedUsers as user (user.id)}
        <div class="flex items-center p-2 bg-gray-100 dark:bg-gray-700 rounded-md relative">
          <div class="relative">
            <img 
              src={user.imageUrl || "https://via.placeholder.com/40"} 
              alt={user.name} 
              class="w-10 h-10 rounded-full object-cover"
            />
            {#if user.isOnline}
              <span class="absolute bottom-0 right-0 block w-3 h-3 bg-green-500 border-2 border-white dark:border-gray-800 rounded-full"></span>
            {:else}
              <span class="absolute bottom-0 right-0 block w-3 h-3 bg-gray-500 border-2 border-white dark:border-gray-800 rounded-full"></span>
            {/if}
          </div>
          <span class="ml-3 text-sm font-medium text-gray-900 dark:text-gray-100">
            {user.name}
          </span>
        </div>
      {/each}
    </div>

    <!-- Settings Button -->
    <button 
      on:click={goToSettings}
      class="mt-4 w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
      ⚙️ Settings
    </button>
  </aside>
</div>

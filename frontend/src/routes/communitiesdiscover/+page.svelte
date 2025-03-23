<script lang="ts">
    import CommunityCard from '$components/communityCard/communityCard.svelte';
  
    let searchQuery: string = "";
  
    // Sample community data with additional cards
    let communities = [
      {
        id: 1,
        name: "Tech Innovators",
        isPublic: true,
        description: "A community for tech enthusiasts who love innovation and emerging technologies.",
        tags: ["#tech", "#innovation", "#ai"],
        degrees: ["Bachelor's", "Master's"],
        totalMembers: 150,
        creationDate: "2025-03-23"
      },
      {
        id: 2,
        name: "Art Lovers",
        isPublic: false,
        description: "A community for art and design lovers looking to share ideas and projects.",
        tags: ["#art", "#design"],
        degrees: ["Bachelor's", "PhD"],
        totalMembers: 80,
        creationDate: "2025-02-15"
      },
      {
        id: 3,
        name: "Gaming Gurus",
        isPublic: true,
        description: "For gamers who are passionate about eSports, streaming, and game development.",
        tags: ["#gaming", "#esports", "#streaming"],
        degrees: ["High School", "Bachelor's"],
        totalMembers: 200,
        creationDate: "2025-01-10"
      },
      {
        id: 4,
        name: "Fitness Freaks",
        isPublic: true,
        description: "A community dedicated to fitness, health, and wellness enthusiasts.",
        tags: ["#fitness", "#health", "#wellness"],
        degrees: ["N/A"],
        totalMembers: 120,
        creationDate: "2025-04-05"
      },
      {
        id: 5,
        name: "Book Club",
        isPublic: false,
        description: "A space for book lovers to discuss literature, share recommendations, and more.",
        tags: ["#books", "#literature", "#reading"],
        degrees: ["N/A"],
        totalMembers: 95,
        creationDate: "2025-03-01"
      }
      // Add more communities if needed.
    ];
  
    // Initially, show all communities
    let filteredCommunities = communities;
  
    function search(): void {
      console.log("Searching for:", searchQuery);
      filteredCommunities = communities.filter(c =>
        c.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
  
    function create(): void {
      console.log("Create button clicked");
      // Add your create logic here
    }
  
    function remove(): void {
      console.log("Remove button clicked");
      // Add your remove logic here
    }
  
    function update(): void {
      console.log("Update button clicked");
      // Add your update logic here
    }
  
    function deleteItem(): void {
      console.log("Delete button clicked");
      // Add your delete logic here
    }
  </script>
  
  <div class="min-h-screen flex flex-col items-center text-gray-900 px-4 sm:px-8 md:px-12 py-12 space-y-12">
 
    <!-- Search Bar -->
    <div class="w-full max-w-lg flex items-center gap-2 border border-gray-300 p-3 rounded-full shadow-sm">
      <input 
        type="text" 
        bind:value={searchQuery} 
        placeholder="Search for a community..." 
        class="w-full text-gray-900 outline-none px-4 bg-transparent"
        on:input={search}
      />
      <button 
        on:click={search} 
        class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-full shadow-md transition"
      >
        Search
      </button>
    </div>
  
    <!-- Community Cards Section -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-full">
      {#each filteredCommunities as community (community.id)}
        <CommunityCard 
          name={community.name}
          isPublic={community.isPublic}
          description={community.description}
          tags={community.tags}
          degrees={community.degrees}
          totalMembers={community.totalMembers}
          creationDate={community.creationDate}
        />
      {/each}
    </div>
  </div>
  
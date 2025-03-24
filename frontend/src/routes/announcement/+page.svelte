<script lang="ts">
  import { onMount } from 'svelte';
  import AnnouncementCard from '$components/announcementCard/announcementCard.svelte';
  import { get } from '$lib/api/get';

  // Define the structure of a global announcement
  interface Announcement {
    id: number;
    title: string;
    description: string;
    tags: string[]; // tags are strings per your API response
    user_id: number;
    uploaded: string;
    edit_user_id: number;
    edit_uploaded: string | null;
    community_id: number;
  }

  // Define the structure of the API response
  interface AnnouncementsResponse {
    global_announcements: Announcement[];
  }

  // Initialize an empty announcements array
  let announcements: Announcement[] = [];

  // Fetch announcements from the API endpoint.
  async function fetchAnnouncements() {
    console.log("Fetching announcements...");

    try {
      const response: unknown = await get('community/announcements');
      console.log("Announcements fetched:", response);

      // Cast the response to the expected type
      const data = response as AnnouncementsResponse;
      announcements = data.global_announcements;
    } catch (error) {
      console.error("Error fetching announcements:", error);
    }
  }

  // Call the function when the component is mounted
  onMount(fetchAnnouncements);
</script>

<main class="container mx-auto px-4 py-4">
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {#if announcements && announcements.length > 0}
      {#each announcements as announcement (announcement.id)}
        <AnnouncementCard
          title={announcement.title}
          description={announcement.description}
          datetime={announcement.uploaded}
        />
      {/each}
    {:else}
      <p>No announcements found.</p>
    {/if}
  </div>
</main>

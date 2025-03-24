<script lang="ts">
    import { onMount } from 'svelte';
    import AnnouncementCard from '$components/announcementCard/announcementCard.svelte';
  
    // Define the structure of a global announcement
    interface Announcement {
      title: string;
      description: string;
      location: string;
      datetime: string;
      duration: number;
      tags: number[];
    }
  
    // Initialize an empty announcements array
    let announcements: Announcement[] = [];
  
    // Fetch announcements from the API endpoint when the component mounts
    onMount(async () => {
      try {
        const response = await fetch('http://localhost:8000/community/events');
        if (!response.ok) {
          throw new Error('Failed to fetch announcements');
        }
        // Assuming the API returns an array of announcements in JSON format
        announcements = await response.json();
      } catch (error) {
        console.error('Error fetching announcements:', error);
      }
    });
  </script>
  
  <main class="container mx-auto px-4 py-4">
    <!-- Responsive grid:
         - 1 column by default,
         - 2 columns on medium screens,
         - 3 columns on large screens -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each announcements as announcement}
        <AnnouncementCard
          title={announcement.title}
          description={announcement.description}
          location={announcement.location}
          datetime={announcement.datetime}
          duration={announcement.duration}
          tags={announcement.tags}
        />
      {/each}
    </div>
  </main>
  

  
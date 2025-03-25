<script lang="ts">

    import AnnouncementCard from '$components/announcementCard/announcementCard.svelte';
    import EventCard from '$components/eventCard/eventCard.svelte';
    import { get } from '$lib/api/get';
	import { onMount } from 'svelte';



</script>

<div class="min-h-screen p-4 sm:p-8 lg:p-12 flex flex-col items-center">
    <!-- Main Content -->
    <main class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-6xl">
        <!-- Announcements -->
        <AnnouncementCard />
        <AnnouncementCard />
        <AnnouncementCard />
		<AnnouncementCard />
		<AnnouncementCard />

        <!-- Events -->
        <EventCard />
        <EventCard />
        <EventCard />
    </main>
</div>

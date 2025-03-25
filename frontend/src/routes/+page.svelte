<script lang="ts">
	import AnnouncementCard from '$components/announcementCard/announcementCard.svelte';
	import EventCard from '$components/eventCard/eventCard.svelte';
	import { get } from '$lib/api/get';
	import { onMount } from 'svelte';
</script>

<div class="flex min-h-screen flex-col items-center p-4 sm:p-8 lg:p-12">
	<!-- Main Content -->
	<main class="grid w-full max-w-6xl grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
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

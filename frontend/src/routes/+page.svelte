<script lang="ts">
	import AnnouncementCard from '$components/announcementCard/announcementCard.svelte';

	import { get } from '$lib/api/get';
	import { onMount } from 'svelte';
	import Feed from '$components/Post/feed.svelte';
	import Post from '$components/Post/post.svelte';

	interface Announcement {
		id: number;
		title: string;
		description: string;
		tags: string[];
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

	let announcements: Announcement[] = [];

	// Fetch announcements from the API endpoint.
	async function fetchAnnouncements() {
		console.log('Fetching announcements...');
		try {
			// Use the generic parameter to directly type the response.
			const data = await get<AnnouncementsResponse>('community/announcements?offset=0&limit=50');
			console.log('Announcements fetched:', data);
			announcements = data.global_announcements;
		} catch (error) {
			console.error('Error fetching announcements:', error);
		}
	}

	onMount(fetchAnnouncements);
</script>

<div class="flex min-h-screen flex-col items-center p-4 sm:p-8 lg:p-12">
	<!-- Main Content -->
	<main class="grid w-full max-w-6xl grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
		<!-- Announcements -->
		{#if announcements.length > 0}
			{#each announcements as announcement (announcement.id)}
				<AnnouncementCard
					title={announcement.title}
					description={announcement.description}
					datetime={announcement.uploaded}
					tags={announcement.tags}
				/>
			{/each}
		{:else}
			<p>No announcements found.</p>
		{/if}
	</main>
	<Feed feedType="posts">
		<Post url="posts/list?offset=0&limit=10" slot="Posts" />
	</Feed>
</div>

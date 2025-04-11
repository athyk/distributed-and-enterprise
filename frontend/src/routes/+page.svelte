
<script lang="ts">
	import AnnouncementCard from '$components/announcementCard/announcementCard.svelte';
	import { get } from '$lib/api/get';
	import { onMount } from 'svelte';
	import Feed from '$components/Post/feed.svelte';
	import Post from '$components/Post/post.svelte';
	import Annoucements from '$components/Post/annoucements.svelte';
	import Event from '$lib/components/Post/event.svelte';

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

<div class="flex min-h-screen bg-gray-100 p-8 sm:p-12 lg:p-20">
	<!-- Two-Column Layout -->
	<div class="mx-auto flex w-full max-w-7xl flex-col lg:flex-row lg:gap-20">
		<!-- Left Column: Announcements -->
		<div class="w-full lg:w-1/3 mb-12 lg:mb-0">
			<div class="space-y-10 p-2">
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
					<div class="flex h-32 items-center justify-center rounded-xl bg-white p-6 shadow-md">
						<p class="text-gray-500">No announcements found.</p>
					</div>
				{/if}
			</div>
		</div>
		
		<!-- Right Column: Posts Feed -->
		<div class="w-full lg:w-2/3">
			<div class="p-2">
				<Feed feedType="posts">
					<Post url="posts/list?offset=0&limit=15" slot="Posts" />
				</Feed>
			</div>
		</div>
	</div>
</div>
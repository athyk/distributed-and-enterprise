
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
	let visibleAnnouncements = 10;
	let loadingMoreAnnouncements = false;

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

	function loadMoreAnnouncements() {
		if (visibleAnnouncements < announcements.length) {
			loadingMoreAnnouncements = true;
			setTimeout(() => {
				visibleAnnouncements += 10;
				loadingMoreAnnouncements = false;
			}, 500);
		}
	}

	// Function to check if we need to load more content when scrolling
	function handleScroll(e) {
		const announcementsContainer = document.getElementById('announcements-container');
		if (!announcementsContainer) return;
		
		const rect = announcementsContainer.getBoundingClientRect();
		const isNearBottom = rect.bottom < window.innerHeight + 200;
		
		if (isNearBottom && !loadingMoreAnnouncements && visibleAnnouncements < announcements.length) {
			loadMoreAnnouncements();
		}
	}

	onMount(() => {
		fetchAnnouncements();
		window.addEventListener('scroll', handleScroll);
		return () => {
			window.removeEventListener('scroll', handleScroll);
		};
	});
</script>

<div class="flex min-h-screen bg-gray-100 px-4 py-6 sm:px-6 sm:py-8 lg:px-8 lg:py-10">
	<!-- Two-Column Layout -->
	<div class="mx-auto flex w-full max-w-7xl flex-col lg:flex-row lg:gap-8 xl:gap-12">
		<!-- Left Column: Announcements -->
		<div class="w-full mb-8 lg:mb-0 lg:w-1/3" id="announcements-container">
			<div class="grid grid-cols-1 gap-4 sm:gap-5">
				{#if announcements.length > 0}
					{#each announcements.slice(0, visibleAnnouncements) as announcement (announcement.id)}
						<AnnouncementCard
							title={announcement.title}
							description={announcement.description}
							datetime={announcement.uploaded}
							tags={announcement.tags}
						/>
					{/each}
					{#if loadingMoreAnnouncements}
						<div class="flex justify-center p-4">
							<div class="loader h-8 w-8 rounded-full border-t-2 border-b-2 border-gray-500 animate-spin"></div>
						</div>
					{/if}
					{#if visibleAnnouncements < announcements.length && !loadingMoreAnnouncements}
						<button 
							class="w-full py-3 text-sm text-gray-600 bg-white rounded-lg shadow-md hover:bg-gray-50"
							on:click={loadMoreAnnouncements}
						>
							Load More Announcements
						</button>
					{/if}
				{:else}
					<div class="flex h-32 items-center justify-center rounded-xl bg-white p-6 shadow-md">
						<p class="text-gray-500">No announcements found.</p>
					</div>
				{/if}
			</div>
		</div>
		
		<!-- Right Column: Posts Feed -->
		<div class="w-full lg:w-2/3">
			<div>
				<Feed feedType="posts">
					<Post url="posts/list?offset=0&limit=50" slot="Posts" />
				</Feed>
			</div>
		</div>
	</div>
</div>

<style>
	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}
	.animate-spin {
		animation: spin 1s linear infinite;
	}
</style>

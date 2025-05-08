<script lang="ts">
	import Feed from '$components/Post/feed.svelte';
	import Post from '$components/Post/post.svelte';
	import Annoucements from '$components/Post/annoucements.svelte';
	import Event from '$lib/components/Post/event.svelte';
	import { getUserInfo } from '$lib/api/checkUser';
	import type { MeResponse, CommunitySearchResponse, communityData } from '$lib/api/apiType';
	import { get } from '$lib/api/get';

	import { onMount } from 'svelte';

	let choice = 0;
	let userUrl = 'https://picsum.photos/id/63/200/200';
	let picture_url = '';

	const tabs = [
		{ label: 'Posts', component: Post, feedType: 'posts', url: 'posts/list' },
		{
			label: 'Events',
			component: Event,
			feedType: 'events',
			url: 'community/events',
			showActions: true
		},
		{
			label: 'Announcements',
			component: Annoucements,
			feedType: 'announcements',
			url: 'community/announcements'
		}
	];

	let author: MeResponse;
	let communities: communityData[] = [];
	let loggedin = false;

	async function fetchUser() {
		try {
			const response = await getUserInfo();
			if (response && response.user) {
				author = response;
				loggedin = true;
			} else {
				throw new Error('Invalid user data');
			}
		} catch (error) {
			console.error('Error fetching user info:', error);
			loggedin = false;
		}
	}

	async function getCommunities() {
		try {
			let response: CommunitySearchResponse = await get(
				'community/search?offset=0&limit=3&is_with=1'
			);
			if (response.success) {
				communities = response.communities;
			} else {
				console.error('Error fetching communities:', response.error_message);
			}
		} catch (error) {
			console.error('Error fetching communities:', error);
		}
	}

	onMount(() => {
		if (localStorage.getItem('loggedin') === 'true') {
			try {
				getCommunities();
				fetchUser();
			} catch (error) {
				console.error('Error parsing user info:', error);
			}
		}
	});
</script>

<div class="flex h-screen flex-col">
	<div class="sticky top-0 z-50 bg-gray-300 shadow-md">
		<div class="flex flex-col items-center pt-5">
			{#if picture_url != ''}
				<a href={userUrl} target="_blank" rel="noopener noreferrer">
					<img src={picture_url} alt="Profile Icon" class="h-11 w-11 rounded-full border" />
				</a>
			{/if}
			<h1 class="pt-5 text-center text-3xl font-bold">
				Welcome {loggedin && author?.user
					? `${author.user.first_name} ${author.user.last_name}`
					: 'Guest'}
			</h1>
		</div>

		<div class="mt-4 flex justify-center border-b border-gray-300">
			{#each tabs as { label }, index}
				<button
					class={`px-4 py-2 text-lg font-semibold ${
						choice === index ? 'border-b-4 border-blue-500 text-blue-500' : 'text-gray-500'
					}`}
					on:click={() => (choice = index)}
				>
					{label}
				</button>
			{/each}
		</div>
	</div>

	<div class="flex flex-1 overflow-hidden">
		<div class="hidden w-1/4 p-4 md:block">
			{#if !loggedin}
				<div class="sticky top-5 rounded-lg border-2 border-gray-300 bg-white p-4 shadow-md">
					<h1 class="text-lg font-bold text-gray-700">Unlock the full potential of UniHub</h1>
					<ul class="mt-2 list-inside list-disc space-y-2 text-gray-600">
						<li>Communicate with fellow Students</li>
						<li>Find out about the latest news</li>
						<li>Join events and activities</li>
					</ul>
					<a
						class="mt-4 block w-full rounded bg-blue-500 px-4 py-2 text-center text-white"
						href="/register"
					>
						Create an account
					</a>
					<p class="mt-2 text-center text-sm text-gray-500">
						Already have an account? <a href="/login" class="text-blue-500">Login</a>
					</p>
				</div>
			{:else}
				<div class="sticky top-5 mt-5 rounded-lg border-2 border-gray-300 bg-white p-4 shadow-md">
					<div class="top-0 flex items-center space-x-2 rounded-t-2xl bg-white">
						{#if author.user.picture_url != ''}
							<a href="/account" target="_blank" rel="noopener noreferrer">
								<img
									src={author.user.picture_url}
									alt="Profile Icon"
									class="h-11 w-11 rounded-full"
								/>
							</a>
						{:else}
							<a href="/account" target="_blank" rel="noopener noreferrer">
								<img
									src="https://picsum.photos/id/63/200/200"
									alt="Profile Icon"
									class="h-11 w-11 rounded-full"
								/>
							</a>
						{/if}
						<span class="font-bold">{author.user.first_name} {author.user.last_name}</span>
						<a
							class="ml-auto block w-1/2 rounded bg-blue-500 px-4 py-2 text-center text-white hover:bg-blue-600"
							href="/account"
						>
							Go To Profile
						</a>
					</div>
				</div>
			{/if}

			<div class="sticky top-5 mt-5 rounded-lg border-2 border-gray-300 bg-white p-4 shadow-md">
				<h1 class="text-lg font-bold text-gray-700">
					{loggedin ? 'My Communities' : 'Communities'}
				</h1>
				<div class="mt-4 space-y-4">
					{#each communities as community}
						<a
							class="block rounded-lg border border-gray-300 bg-gray-100 p-4 transition-shadow hover:shadow-lg"
							href="/communities/{community.id}"
						>
							<h2 class="font-semibold text-gray-800">{community.name}</h2>
							<p class="mt-1 text-sm text-gray-600">{community.member_count} members</p>
							<p class="mt-1 text-sm text-gray-600">{community.description}</p>
						</a>
					{/each}
				</div>
				<a
					class="mt-4 block w-full rounded bg-blue-500 px-4 py-2 text-center text-white hover:bg-blue-600"
					href="/communities"
				>
					View More
				</a>
			</div>
		</div>

		<div class="scrollbar-none mt-2 flex w-full justify-center overflow-y-auto px-4 md:w-1/2">
			<div class="w-full max-w-2xl">
				{#if choice === 0}
					<div class="w-full">
						<Feed feedType="posts">
							<Post url="posts/list" slot="Posts" limit={30} />
						</Feed>
					</div>
				{:else if choice === 1}
					<div class="w-full">
						<Feed feedType="events" showActions={true} communityID={1}>
							<Event url="community/events" slot="Posts" limit={30} />
						</Feed>
					</div>
				{:else if choice === 2}
					<div class="w-full">
						<Feed feedType="announcements">
							<Annoucements url="community/announcements" slot="Posts" limit={30} />
						</Feed>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>

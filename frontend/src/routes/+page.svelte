<script lang="ts">
	import Feed from '$components/Post/feed.svelte';
	import Post from '$components/Post/post.svelte';
	import Annoucements from '$components/Post/annoucements.svelte';
	import Event from '$lib/components/Post/event.svelte';

	import { onMount } from 'svelte';

	let choice = 0;
	let name = '';
	let userUrl = 'https://picsum.photos/id/63/200/200'; // Default/placeholder
	let picture_url = '';
	let isLoggedIn = false; // <-- New state variable

	const tabs = [
		{ label: 'Posts', component: Post, feedType: 'posts', url: 'posts/list' },
		{ label: 'Events', component: Event, feedType: 'events', url: 'community/events', showActions: true },
		{ label: 'Announcements', component: Annoucements, feedType: 'announcements', url: 'community/announcements' }
	];

	const communities = [
		{ name: 'Community 1', description: 'Description Text Here', member_count: 10 },
		{ name: 'Community 2', description: 'Another description here.', member_count: 5 },
		{ name: 'Community 3', description: 'Yet another description.', member_count: 20 }
	];

	const recent_Posts = [
		{ name: 'Post 1', created_at: '1742949086', description: 'Description Text Here' },
		{ name: 'Post 2', created_at: '1742949086', description: 'Another description here.' },
		{ name: 'Post 3', created_at: '1742949086', description: 'Yet another description.' }
	];

	//localhost:8000/community/search?offset=0&limit=10&is_with=1
	//localhost:8000/posts/list?user_id=1&offset=0&limit=5

	onMount(() => {
		if (localStorage.getItem('loggedin') === 'true') {
			const userInfo = localStorage.getItem('userInfo');
			try {
				if (userInfo) { // Check if userInfo actually exists
					let user = JSON.parse(userInfo).user;
					name = user.first_name + ' ' + user.last_name;
					picture_url = user.picture_url;
					userUrl = '/user/' + user.id.toString();
					isLoggedIn = true; // <-- Set logged in state to true
				} else {
					// Handle case where 'loggedin' is true but 'userInfo' is missing
					console.warn('Logged in flag set, but user info missing from localStorage.');
					name = 'User'; // Or some other placeholder
					isLoggedIn = true; // Still technically logged in according to flag
				}
			} catch (error) {
				console.error('Error parsing user info:', error);
				name = 'Guest';
				isLoggedIn = false; // <-- Set logged in state to false on error
                // Optionally clear potentially corrupted localStorage items
                // localStorage.removeItem('loggedin');
                // localStorage.removeItem('userInfo');
			}
		} else {
			name = 'Guest';
			isLoggedIn = false; // <-- Set logged in state to false
		}
	});
</script>

<div class="flex flex-col h-screen">
	<div class="sticky top-0 bg-white z-50 shadow-md"> <!-- Changed bg to white for better contrast -->
		<div class="flex flex-col items-center pt-5">
			{#if picture_url} <!-- Simplified check for picture_url -->
				<a href={userUrl} target="_blank" rel="noopener noreferrer">
					<img src={picture_url} alt="Profile Icon" class="h-11 w-11 rounded-full border object-cover" /> <!-- Added object-cover -->
				</a>
			{:else if isLoggedIn}
                <!-- Optional: Show a default avatar if logged in but no picture -->
                <div class="h-11 w-11 rounded-full border bg-gray-300 flex items-center justify-center text-gray-600 text-xl font-semibold">
                    {name.charAt(0).toUpperCase()} <!-- Display first initial -->
                </div>
            {/if}
			<h1 class="pt-5 text-center text-3xl font-bold text-gray-800">Welcome {name}</h1> <!-- Adjusted text color -->
		</div>

		<div class="mt-4 flex justify-center border-b border-gray-200"> <!-- Lighter border -->
			{#each tabs as { label }, index}
				<button
					class={`px-4 py-2 text-lg font-semibold transition-colors duration-200 ${
						choice === index ? 'border-b-4 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
					}`}
					on:click={() => (choice = index)}
				>
					{label}
				</button>
			{/each}
		</div>
	</div>

	<div class="flex flex-1 overflow-hidden bg-gray-100"> <!-- Added background color to main content area -->
		<!-- Left Sidebar -->
		<div class="w-1/4 p-4 hidden md:block overflow-y-auto scrollbar-thin"> <!-- Added overflow & scrollbar -->
			<!-- Conditional Login/Register Prompt -->
			{#if !isLoggedIn}
				<div class="rounded-lg border border-gray-200 bg-white p-4 shadow-md sticky top-5 mb-5">
					<h1 class="text-lg font-bold text-gray-700">Unlock the full potential of UniHub</h1>
					<ul class="mt-2 space-y-2 list-disc list-inside text-gray-600">
						<li>Communicate with fellow Students</li>
						<li>Find out about the latest news</li>
						<li>Join events and activities</li>
					</ul>
					<a class="mt-4 block w-full rounded bg-blue-500 px-4 py-2 text-center text-white hover:bg-blue-600 transition-colors" href="/register">
						Create an account
					</a>
					<p class="mt-2 text-center text-sm text-gray-500">
						Already have an account? <a href="/login" class="text-blue-500 hover:underline">Login</a>
					</p>
				</div>
			{/if}

			<!-- Recent Posts (Always Visible) -->
			<div class="rounded-lg border border-gray-200 bg-white p-4 shadow-md sticky top-5"> <!-- Removed mt-5 if login prompt hidden -->
				<h1 class="text-lg font-bold text-gray-700">My Recent Posts</h1>
				<div class="mt-4 space-y-4">
					{#each recent_Posts as post}
						<div class="rounded-lg border border-gray-300 bg-gray-50 p-3 hover:shadow-lg transition-shadow"> <!-- Adjusted padding/bg -->
							<h2 class="text-gray-800 font-semibold">{post.name}</h2>
							<p class="mt-1 text-sm text-gray-600 truncate">{post.description}</p> <!-- Added truncate -->
						</div>
					{/each}
				</div>
				{#if isLoggedIn} <!-- Only show View All if logged in? Adjust if needed -->
					<a class="mt-4 block w-full rounded bg-blue-500 px-4 py-2 text-center text-white hover:bg-blue-600 transition-colors" href="/posts"> <!-- Assuming a /posts page exists -->
						View All My Posts
					</a>
				{/if}
			</div>
		</div>

		<!-- Main Content Feed -->
		<div class="w-full md:w-1/2 px-4 overflow-y-auto scrollbar-thin"> <!-- Added scrollbar-thin -->
			<div class="min-h-screen py-4"> <!-- Added padding -->
				{#if choice === 0}
					<div class="w-full max-w-4xl mx-auto"> <!-- Centered content -->
						<Feed feedType="posts">
							<Post url="posts/list" slot="Posts" limit={30} />
						</Feed>
					</div>
				{:else if choice === 1}
					<div class="w-full max-w-4xl mx-auto"> <!-- Centered content -->
						<Feed feedType="events" showActions={true} communityID={1}>
							<Event url="community/events" slot="Posts" limit={30} />
						</Feed>
					</div>
				{:else if choice === 2}
					<div class="w-full max-w-4xl mx-auto"> <!-- Centered content -->
						<Feed feedType="announcements">
							<Annoucements url="community/announcements" slot="Posts" limit={30} />
						</Feed>
					</div>
				{/if}
			</div>
		</div>

		<!-- Right Sidebar -->
		<div class="w-1/4 p-4 hidden md:block overflow-y-auto scrollbar-thin"> <!-- Added overflow & scrollbar -->
			<div class="rounded-lg border border-gray-200 bg-white p-4 shadow-md sticky top-5">
				<h1 class="text-lg font-bold text-gray-700">My Top Communities</h1>
				<div class="mt-4 space-y-4">
					{#each communities as community}
						<div class="rounded-lg border border-gray-300 bg-gray-50 p-3 hover:shadow-lg transition-shadow"> <!-- Adjusted padding/bg -->
							<h2 class="text-gray-800 font-semibold ">{community.name}</h2>
							<p class="mt-1 text-sm text-gray-600">{community.member_count} members</p>
							<p class="mt-1 text-sm text-gray-600 truncate">{community.description}</p> <!-- Added truncate -->
							<a class="mt-2 text-blue-500 hover:underline text-sm" href="/community/{community.name}"> <!-- Smaller text -->
								Go to community
							</a>
						</div>
					{/each}
				</div>
				<a class="mt-4 block w-full rounded bg-blue-500 px-4 py-2 text-center text-white hover:bg-blue-600 transition-colors" href="/communities">
					Find More Communities
				</a>
			</div>
		</div>
	</div>
</div>
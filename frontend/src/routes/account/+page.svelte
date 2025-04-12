<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import Feed from '$components/Post/feed.svelte';
	import Announcements from '$components/Post/annoucements.svelte';
	import Post from '$components/Post/post.svelte';
	import Event from '$lib/components/Post/event.svelte';
	import { get } from '$lib/api/get';

	// Define a TypeScript interface for the user data.
	interface User {
		id: number;
		email: string;
		email_verified: number;
		first_name: string;
		last_name: string;
		gender: string;
		date_of_birth: string;
		picture_url: string;
		degree_id: number;
		year_of_study: number;
		grad_date: string;
		tags: number[];
		rank?: string;
		created_at?: number;
		updated_at?: number;
	}

	// Create a writable store to hold the user data.
	const userStore = writable<User | null>(null);

	// Function to fetch user data from the API endpoint.
	async function fetchUser() {
		try {
			// The response now is expected to have the shape { success: boolean, user: User }
			const data = await get<{ success: boolean; user: User }>('users/@me');
			// Set the user data from the nested "user" property.
			userStore.set(data.user);
			console.log('User data loaded:', data.user);
		} catch (error) {
			console.error('Error fetching user:', error);
		}
	}

	// Choice variable (used to toggle between different post panels).
	let choice = 0;

	// Fetch user data when the component mounts.
	onMount(() => {
		fetchUser();
	});
</script>

<main class="settings-page" style="padding: 20px; font-family: Arial, sans-serif;">
	<h1>User Settings</h1>

	{#if $userStore}
		<section class="user-info" style="margin-bottom: 40px;">
			<h2>Profile Information</h2>
			<p><strong>Email:</strong> {$userStore.email}</p>
			<p>
				<strong>Email Verified:</strong> {$userStore.email_verified ? 'Yes' : 'No'}
			</p>
			<p><strong>First Name:</strong> {$userStore.first_name}</p>
			<p><strong>Last Name:</strong> {$userStore.last_name}</p>
			<p><strong>Gender:</strong> {$userStore.gender}</p>
			<p><strong>Date of Birth:</strong> {$userStore.date_of_birth}</p>
			{#if $userStore.picture_url}
				<img src={$userStore.picture_url} alt="User profile" style="width: 150px; height: 150px;" />
			{:else}
				<p><em>No profile picture available.</em></p>
			{/if}
			<p><strong>Degree ID:</strong> {$userStore.degree_id}</p>
			<p><strong>Year of Study:</strong> {$userStore.year_of_study}</p>
			<p><strong>Graduation Date:</strong> {$userStore.grad_date}</p>
			<p><strong>Tags:</strong> {$userStore.tags.join(', ')}</p>
		</section>
	{:else}
		<p>Loading user data...</p>
	{/if}

	<!-- Testing section for switching feeds -->
	<h1 class="pt-5 text-center text-3xl font-bold">Testing</h1>
	<div class="mt-4 flex items-center justify-center">
		<input
			type="button"
			class="rounded bg-blue-500 px-4 py-2 text-white"
			value="Posts"
			on:click={() => (choice = 0)}
		/>
		<input
			type="button"
			class="m-2 rounded bg-blue-500 px-4 py-2 text-white"
			value="Events Community 1"
			on:click={() => (choice = 1)}
		/>
		<input
			type="button"
			class="rounded bg-blue-500 px-4 py-2 text-white"
			value="Annoucements"
			on:click={() => (choice = 2)}
		/>
	</div>

	<div class="flex min-h-screen items-center justify-center px-4">
		{#if choice === 0}
			<div class="w-full max-w-4xl">
				<Feed feedType="posts">
					<Post url="posts/list" slot="Posts" limit={30} />
				</Feed>
			</div>
		{:else if choice === 1}
			<div class="w-full max-w-4xl">
				<Feed feedType="events" showActions={true} communityID={5}>
					<Event url="community/1/events" slot="Posts" limit={30} />
				</Feed>
			</div>
		{:else if choice === 2}
			<div class="w-full max-w-4xl">
				<Feed feedType="announcements">
					<Announcements url="community/announcements" slot="Posts" limit={30} />
				</Feed>
			</div>
		{/if}
	</div>
</main>

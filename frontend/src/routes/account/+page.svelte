<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import { get } from '$lib/api/get';
	import { Put } from '$lib/api/Put';

	// Define the TypeScript interface for User.
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

	// Create a writable store for user data.
	const userStore = writable<User | null>(null);

	// Local reactive object for managing form data.
	let userData: User = {
		id: 0,
		email: '',
		email_verified: 0,
		first_name: '',
		last_name: '',
		gender: '',
		date_of_birth: '',
		picture_url: '',
		degree_id: 0,
		year_of_study: 0,
		grad_date: '',
		tags: [],
		rank: 'user'
	};

	// Variables for password update.
	let password: string = '';
	let new_password: string = '';

	// Fetch user data when the component mounts.
	async function fetchUser() {
		try {
			// Expected return shape: { success: boolean, user: User }
			const data = await get<{ success: boolean; user: User }>('users/@me');
			userStore.set(data.user);
			userData = { ...data.user };
			console.log('User data loaded:', data.user);
		} catch (error) {
			console.error('Error fetching user:', error);
		}
	}

	// Update settings by sending a PUT request.
	async function updateSettings() {
		// Convert tags from comma separated string to number array.
		userData.tags = parseTags(tagsString);
		const payload = {
			...userData,
			password,
			new_password
		};

		try {
			const res = await Put<{ success: boolean; user: User }>('users/', payload);
			if (res.success) {
				userStore.set(res.user);
				userData = { ...res.user };
				alert('Settings updated successfully.');
				password = '';
				new_password = '';
			} else {
				alert('Failed to update settings.');
			}
		} catch (error) {
			console.error('Error updating settings:', error);
			alert('An error occurred while updating settings.');
		}
	}

	// Helper function to parse tags.
	function parseTags(tagsStr: string): number[] {
		return tagsStr
			.split(',')
			.map(tag => parseInt(tag.trim()))
			.filter(num => !isNaN(num));
	}

	// Tag input string for binding.
	let tagsString: string = '';
	$: if (userData.tags && userData.tags.length > 0) {
		tagsString = userData.tags.join(', ');
	}

	// Fetch the user data when the component mounts.
	onMount(() => {
		fetchUser();
	});
</script>

<main class="flex items-center justify-center min-h-screen bg-gray-50 p-6">
	<div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
		<h1 class="text-2xl font-bold text-center text-gray-800 mb-6">User Settings</h1>
		{#if $userStore}
			<form on:submit|preventDefault={updateSettings} class="space-y-4">
				<!-- Email -->
				<div>
					<label for="email" class="block text-sm font-medium text-gray-700">Email:</label>
					<input
						id="email"
						type="email"
						bind:value={userData.email}
						class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
					/>
				</div>

				<!-- Email Verified -->
				<div class="flex items-center">
				
				</div>

				<!-- First Name -->
				<div>
					<label for="first_name" class="block text-sm font-medium text-gray-700">First Name:</label>
					<input
						id="first_name"
						type="text"
						bind:value={userData.first_name}
						class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
					/>
				</div>

				<!-- Last Name -->
				<div>
					<label for="last_name" class="block text-sm font-medium text-gray-700">Last Name:</label>
					<input
						id="last_name"
						type="text"
						bind:value={userData.last_name}
						class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
					/>
				</div>

				<!-- Gender -->
				<div>
					<label for="gender" class="block text-sm font-medium text-gray-700">Gender:</label>
					<input
						id="gender"
						type="text"
						bind:value={userData.gender}
						class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
					/>
				</div>

				<!-- Date of Birth -->
				<div>
					<label for="date_of_birth" class="block text-sm font-medium text-gray-700">Date of Birth:</label>
					<input
						id="date_of_birth"
						type="date"
						bind:value={userData.date_of_birth}
						class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
					/>
				</div>

				<!-- Degree ID -->
				<div>
					<label for="degree_id" class="block text-sm font-medium text-gray-700">Degree ID:</label>
					<input
						id="degree_id"
						type="number"
						bind:value={userData.degree_id}
						class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
					/>
				</div>

				<!-- Year of Study -->
				<div>
					<label for="year_of_study" class="block text-sm font-medium text-gray-700">Year of Study:</label>
					<input
						id="year_of_study"
						type="number"
						bind:value={userData.year_of_study}
						class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
					/>
				</div>

				<!-- Graduation Date -->
				<div>
					<label for="grad_date" class="block text-sm font-medium text-gray-700">Graduation Date:</label>
					<input
						id="grad_date"
						type="date"
						bind:value={userData.grad_date}
						class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
					/>
				</div>

				<!-- Tags -->
				<div>
					<label for="tags" class="block text-sm font-medium text-gray-700">Tags:</label>
					<input
						id="tags"
						type="text"
						bind:value={tagsString}
						placeholder="E.g., 1, 2, 3"
						class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
					/>
				</div>

				<!-- Rank -->
				<div>
					<label for="rank" class="block text-sm font-medium text-gray-700">Rank:</label>
					<input
						id="rank"
						type="text"
						bind:value={userData.rank}
						class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
					/>
				</div>

				<!-- Password Fields -->
				<div>
					<label for="password" class="block text-sm font-medium text-gray-700">Current Password:</label>
					<input
						id="password"
						type="password"
						bind:value={password}
						class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
					/>
				</div>
				<div>
					<label for="new_password" class="block text-sm font-medium text-gray-700">New Password:</label>
					<input
						id="new_password"
						type="password"
						bind:value={new_password}
						class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300"
					/>
				</div>

				<!-- Submit Button -->
				<div>
					<button
						type="submit"
						class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-md focus:outline-none focus:ring focus:border-blue-300"
					>
						Save Changes
					</button>
				</div>
			</form>
		{:else}
			<p class="text-center text-gray-600">Loading user data...</p>
		{/if}
	</div>
</main>

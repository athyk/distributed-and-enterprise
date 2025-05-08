<script lang="ts">
	import { onMount } from 'svelte';
	import { getUserInfo } from '$lib/api/checkUser';
	import type { MeResponse } from '$lib/api/apiType';
	import { getDegreeName } from '$lib/api/getDegreeID';
	import { getTagName } from '$lib/api/getTagID';
	import UserEditModal from './userEditModal.svelte';
	import { get } from '$lib/api/get';
	import { isUserID } from '$lib/api/checkUser';

	export let user_id: number | null = null;
	export let self = false;
	let userInfo: MeResponse;
	let degree_name: string | undefined = undefined;
	let modalShown = false;
	let dataloaded = false;
	export let refreshKey = 0;

	function showModal() {
		modalShown = true;
	}

	async function formatDegree(degree_id: number | string) {
		try {
			if (typeof degree_id === 'number') {
				degree_id = degree_id.toString();
			}
			const result = await getDegreeName(degree_id);
			degree_name = result !== -1 ? result : undefined;
		} catch (error) {
			console.error('Error fetching degree name:', error);
		}
	}

	onMount(async () => {
		console.warn('user_id:', user_id);
		if (user_id !== null && (await isUserID(user_id))) {
			self = true;
		}
		if (!self) {
			getUser();
			dataloaded = true;
			return;
		}
		const response = (await getUserInfo()) as MeResponse;
		if (response.success === true) {
			user_id = response.user.id;
			userInfo = response;
			formatDegree(userInfo.user.degree_id);
			dataloaded = true;
		} else {
			console.error('Error fetching user info:', response.error_message);
		}
	});

	async function getUser() {
		console.log('Fetching user data...');
		try {
			const response = (await get('users/?user_id=' + user_id)) as MeResponse;
			if (response.success === true) {
				console.log('User data fetched successfully:', response.users[0]);
				user_id = response.users[0].id;
				formatDegree(response.users[0].degree_id);
				userInfo = {
					user: response.users[0],
					users: response.users,
					success: true,
					error_message: ''
				};
				dataloaded = true;
			} else {
				console.error('Error fetching user info:', response.error_message);
			}
		} catch (error) {
			console.error('Failed to fetch user data:', error);
		}
	}

	async function refreshUserData() {
		try {
			const response = (await getUserInfo()) as MeResponse;
			if (response.success === true) {
				user_id = response.user.id;
				userInfo = response;
				formatDegree(userInfo.user.degree_id);
				dataloaded = true;
			} else {
				console.error('Error refreshing user info:', response.error_message);
			}
		} catch (error) {
			console.error('Failed to refresh user data:', error);
		}
	}

	$: if (refreshKey > 0) {
		console.log('Refreshing user data...');
		refreshUserData();
	}
</script>

{#if dataloaded && userInfo && userInfo.user}
	<div
		class="mb-4 flex flex-col items-center gap-3 border-b border-gray-300 pt-5 pb-4 sm:flex-row sm:items-start"
	>
		<div class="mb-2 flex-shrink-0 sm:mb-0">
			{#if userInfo.user.picture_url}
				<img
					src={userInfo.user.picture_url}
					alt="Profile"
					class="h-16 w-16 rounded-full border-2 border-gray-200 sm:h-20 sm:w-20"
				/>
			{:else}
				<img
					src="https://picsum.photos/id/63/200/200"
					alt="Profile"
					class="h-16 w-16 rounded-full border-2 border-gray-200 sm:h-20 sm:w-20"
				/>
			{/if}
		</div>
		<div class="flex flex-col text-center sm:text-left">
			<h1 class="text-xl font-bold sm:text-2xl">
				{userInfo.user.first_name}
				{userInfo.user.last_name}
			</h1>
			<p class="text-gray-700">Year {userInfo.user.year_of_study} {degree_name} Student</p>
		</div>
		{#if self}
			<div class="mt-2 sm:mt-0 sm:ml-auto">
				<button
					on:click={showModal}
					class="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
				>
					Edit Account
				</button>
			</div>
		{/if}
	</div>
	<div class="mb-4 rounded-lg border border-gray-300 bg-gray-50 p-4">
		<ul class="space-y-3">
			<li>
				<strong>Member Since:</strong>
				{new Date(Number(userInfo.user.created_at) * 1000).toLocaleDateString()}
			</li>
			<li>
				<strong>Tags:</strong>
				<div class="mt-1 flex flex-wrap gap-2">
					{#if userInfo.user.tags?.length}
						{#each userInfo.user.tags as tag}
							{#await getTagName(tag.toString()) then tagName}
								<span class="rounded-md bg-gray-200 px-2 py-1 text-sm">{tagName}</span>
							{:catch}
								<span class="rounded-md bg-red-200 px-2 py-1 text-sm">Error</span>
							{/await}
						{/each}
					{:else}
						<span>None</span>
					{/if}
				</div>
			</li>
			<li><strong>Gender:</strong> {userInfo.user.gender || 'Not specified'}</li>
		</ul>
	</div>
	<UserEditModal
		bind:modalShown
		bind:refreshKey
		{userInfo}
		on:close={() => (modalShown = false)}
		on:refresh={() => (refreshKey += 1)}
	/>
{/if}

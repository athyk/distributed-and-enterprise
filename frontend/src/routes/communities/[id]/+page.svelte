<script lang="ts">
	import Feed from '$components/Post/feed.svelte';
	import Annoucements from '$components/Post/annoucements.svelte';
	import Event from '$lib/components/Post/event.svelte';
	import { getUserInfo } from '$lib/api/checkUser';
	import type {
		MeResponse,
		communityData,
		response,
		StudentSearchResponse
	} from '$lib/api/apiType';
	import { get } from '$lib/api/get';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import EditCommunityCard from '$components/communityCRUD/edit.svelte';
	import { checkPermisions, isWithCommunity, isRequested, isAdmin } from '$lib/api/checkUser';
	import { post } from '$lib/api/post';
	import { deleteCall } from '$lib/api/delete';
	import Popup from '$components/ErrorPopUp/popup.svelte';

	let choice = 0;
	let userUrl = 'https://picsum.photos/id/63/200/200';
	let picture_url = '';
	let communityId: string;
	let int_communityId: number;
	let modalShown = false;
	let hasPermission = false;
	let inCommunity = false;
	let author: MeResponse;
	let community: communityData;
	let communityFetched = false;
	let loggedin = false;
	let errorMessage = '';
	let private_community = false;
	let requested_users_view = 0;
	let users_fetched = false;
	let refreshCommunity = 0;
	let hasRequested = false;
	let isAadmin = false;
	let usersID = -1;

	let users: {
		id: number;
		name: string;
	}[] = [];

	let moderator_users: {
		id: number;
		name: string;
	}[] = [];

	let admin_users: {
		id: number;
		name: string;
	}[] = [];

	let requested_users: {
		id: number;
		name: string;
	}[] = [];

	let banned_users: {
		id: number;
		name: string;
	}[] = [];

	const tabs = [{ label: 'Events' }, { label: 'Announcements' }];

	async function getName(id: number) {
		try {
			const response: StudentSearchResponse = await get('users/?user_id=' + id);
			if (response.success) {
				return response.users[0].first_name + ' ' + response.users[0].last_name;
			} else {
				console.error('Error fetching user name:', response.error_message);
				return 'Unknown User';
			}
		} catch (error) {
			console.error('Error fetching user name:', error);
			return 'Unknown User';
		}
	}

	async function getUsers() {
		users_fetched = false;
		users = [];
		admin_users = [];
		moderator_users = [];
		requested_users = [];
		try {
			const response = await get('community/' + communityId + '/get_all');
			if (response.success) {
				console.log('Users:', response.all_users);

				const userPromises = response.all_users
					.filter((user) => user[1] === 'user')
					.map(async (user) => ({
						id: user[0],
						name: await getName(user[0])
					}));

				const adminPromises = response.all_users
					.filter((user) => user[1] === 'admin')
					.map(async (user) => ({
						id: user[0],
						name: await getName(user[0])
					}));

				const moderatorPromises = response.all_users
					.filter((user) => user[1] === 'moderator')
					.map(async (user) => ({
						id: user[0],
						name: await getName(user[0])
					}));

				const bannedPromises = response.all_users
					.filter((user) => user[1] === 'banned')
					.map(async (user) => ({
						id: user[0],
						name: await getName(user[0])
					}));

				users = await Promise.all(userPromises);
				admin_users = await Promise.all(adminPromises);
				moderator_users = await Promise.all(moderatorPromises);
				banned_users = await Promise.all(bannedPromises);

				if (private_community) {
					try {
						console.log('Fetching requested users...');

						const requestedPromises = response.all_users
							.filter((user) => user[1] === 'requested')
							.map(async (user) => ({
								id: user[0],
								name: await getName(user[0]),
								role: user[1]
							}));
						requested_users = await Promise.all(requestedPromises);
					} catch (error) {
						console.error('Error fetching requested users:', error);
					}
				}
				console.log('Booooooooooooooooooooo');
				users_fetched = true;
				console.log('Users:', users);
				console.log('Admin Users:', admin_users);
				console.log('Moderator Users:', moderator_users);
				console.log('Requested Users:', requested_users);
			} else {
				console.error('Error fetching users:', response.error_message);
			}
		} catch (error) {
			console.error('Error fetching users:', error);
		}
	}

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

	async function getCommunity() {
		try {
			let response: communityData = await get('community/' + communityId);
			console.log('Community response:', response);
			if (response.success) {
				community = response;
				private_community = !response.public_community;
				communityFetched = true;
			}
		} catch (error) {
			console.error('Error fetching community:', error);
		}
	}

	async function joinCommunity() {
		try {
			const response: response = await post('community/' + communityId + '/members', {});
			if (response.success) {
				console.log('Joined community successfully');
				if (private_community) {
					errorMessage = 'Request sent to join the community.';
					hasRequested = true;
				} else {
					inCommunity = true;
				}
			} else {
				console.error('Error joining community:', response.error_message);
				errorMessage = response.error_message[0];
			}
		} catch (error) {
			console.error('Error joining community:', error);
			errorMessage = 'Error joining community';
		}
	}

	async function leaveCommunity() {
		try {
			const response: response = await deleteCall('community/' + communityId + '/members', {});
			if (response.success) {
				console.log('left community successfully');
				inCommunity = false;
				if (private_community) {
					hasRequested = false;
					communityFetched = false;
				}
			} else {
				console.error('Error leaving community:', response.error_message);
				errorMessage = response.error_message[0];
			}
		} catch (error) {
			console.error('Error leaving community:', error);
			errorMessage = 'Error leavi community';
		}
	}

	async function premoteUser(userId: number) {
		try {
			const response: response = await post('community/' + communityId + '/promote', {
				action_user_id: userId
			});
			if (response.success) {
				console.log('User promoted successfully');
				getUsers();
			} else {
				console.error('Error promoting user:', response.error_message);
				errorMessage = response.error_message[0];
			}
		} catch (error) {
			console.error('Error promoting user:', error);
			errorMessage = 'Error promoting user';
		}
	}

	async function demoteUser(userId: number) {
		try {
			const response: response = await post('community/' + communityId + '/demote', {
				action_user_id: userId
			});
			if (response.success) {
				console.log('User demoted successfully');
				getUsers();
			} else {
				console.error('Error demoting user:', response.error_message);
				errorMessage = response.error_message[0];
			}
		} catch (error) {
			console.error('Error demoting user:', error);
			errorMessage = 'Error demoting user';
		}
	}

	async function banUser(userId: number) {
		try {
			const response: response = await post('community/' + communityId + '/ban', {
				action_user_id: userId
			});
			if (response.success) {
				console.log('User banned successfully');
				getUsers();
			} else {
				console.error('Error banning user:', response.error_message);
				errorMessage = response.error_message[0];
			}
		} catch (error) {
			console.error('Error banning user:', error);
			errorMessage = 'Error banning user';
		}
	}

	async function addUser(userId: number) {
		try {
			const response: response = await post('community/' + communityId + '/invite', {
				invite_user_id: userId
			});
			if (response.success) {
				console.log('User added successfully');
				getUsers();
			} else {
				console.error('Error adding user:', response.error_message);
				errorMessage = response.error_message[0];
			}
		} catch (error) {
			console.error('Error adding user:', error);
			errorMessage = 'Error adding user';
		}
	}

	onMount(async () => {
		if (localStorage.getItem('loggedin') === 'true') {
			communityFetched = false;
			users_fetched = false;
			hasRequested = false;
			errorMessage = '';
			try {
				communityId = $page.params.id;
				int_communityId = parseInt(communityId);
				if (await checkPermisions(parseInt(communityId))) {
					console.log('User has permissions to edit the community.');
					hasPermission = true;
					if (await isAdmin(parseInt(communityId))) {
						console.log('User is an admin of the community.');
						isAadmin = true;
					} else {
						console.log('User is not an admin of the community.');
						isAadmin = false;
					}
				} else {
					console.log('User does not have permissions to edit the community.');
					hasPermission = false;
				}

				const response = await getUserInfo();
				usersID = response.user.id;

				if (await isWithCommunity(parseInt(communityId))) {
					console.log('User is in the community.');
					if (await isRequested(parseInt(communityId))) {
						console.log('User has requested to join the community.');
						hasRequested = true;
					} else {
						console.log('User is already a member of the community.');
						inCommunity = true;
					}
				} else {
					console.log('User is not in the community.');
					inCommunity = false;
				}

				getCommunity();
				fetchUser();
				getUsers();
			} catch (error) {
				console.error('Error parsing user info:', error);
			}
		} else {
			window.location.href = '/';
		}
	});

	$: if (refreshCommunity > 0) {
		getCommunity();
		getUsers();
		refreshCommunity = 0;
	}
</script>

{#if communityFetched}
	<EditCommunityCard bind:modalShown communityID={parseInt(communityId)} bind:refreshCommunity />
{/if}

{#if loggedin}
	{#if author.user.picture_url != ''}
		<script>
			userUrl = author.user.picture_url;
			picture_url = author.user.picture_url;
		</script>
	{:else}
		<script>
			userUrl = 'https://picsum.photos/id/63/200/200';
			picture_url = 'https://picsum.photos/id/63/200/200';
		</script>
	{/if}
{/if}
<div class="flex h-screen flex-col">
	<Popup bind:errorMessage />
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

	{#if loggedin}
		<div class="flex flex-1 overflow-hidden">
			<div class="hidden w-1/4 p-4 md:block">
				{#if loggedin}
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
					{#if communityFetched}
						<h1 class="text-lg font-bold text-gray-700">
							{community.name}
							{#if private_community}
								(Private)
							{/if}
						</h1>
						<div class="mt-4 space-y-4">
							<div
								class="rounded-lg border border-gray-300 bg-gray-100 p-4 transition-shadow hover:shadow-lg"
							>
								<p class="mt-1 text-sm text-gray-600">{community.description}</p>
							</div>
						</div>
					{/if}
					{#if inCommunity}
						<button
							class="mt-4 block w-full rounded bg-blue-500 px-4 py-2 text-center text-white hover:bg-red-600"
							on:click={() => leaveCommunity()}
						>
							Leave
						</button>
					{:else if private_community && hasRequested}
						<button
							class="mt-4 block w-full cursor-not-allowed rounded bg-gray-400 px-4 py-2 text-center text-white"
						>
							Requested
						</button>
					{:else}
						<button
							class="mt-4 block w-full rounded bg-blue-500 px-4 py-2 text-center text-white hover:bg-green-600"
							on:click={() => joinCommunity()}
						>
							{private_community ? 'Request' : 'Join'}
						</button>
					{/if}
					{#if hasPermission}
						<button
							class="mt-4 block w-full rounded bg-blue-500 px-4 py-2 text-center text-white hover:bg-blue-600"
							on:click={() => (modalShown = true)}
						>
							Edit
						</button>
					{/if}
				</div>

				{#if inCommunity || !private_community}
					<div class="sticky top-5 mt-5 rounded-lg border-2 border-gray-300 bg-white p-4 shadow-md">
						{#if communityFetched}
							<h1 class="text-lg font-bold text-gray-700">Members</h1>
							{#if hasPermission}
								<div class="m-4 flex justify-between">
									<button
										class="w-1/2 rounded {requested_users_view === 0
											? 'bg-blue-500 hover:bg-blue-600'
											: 'bg-gray-300 hover:bg-gray-400'} mr-1 px-2 py-1 text-center text-white"
										on:click={() => (requested_users_view = 0)}
									>
										Members
									</button>
									{#if private_community}
										{#if hasPermission}
											<button
												class="w-1/2 rounded {requested_users_view === 1
													? 'bg-blue-500 hover:bg-blue-600'
													: 'bg-gray-300 hover:bg-gray-400'} ml-1 px-2 py-1 text-center text-white"
												on:click={() => (requested_users_view = 1)}
											>
												Requested
											</button>
										{/if}
									{/if}
									{#if isAadmin}
										<button
											class="w-1/2 rounded {requested_users_view === 2
												? 'bg-red-500 hover:bg-red-600'
												: 'bg-red-300 hover:bg-red-400'} ml-1 px-2 py-1 text-center text-white"
											on:click={() => (requested_users_view = 2)}
										>
											Banned Users
										</button>
									{/if}
								</div>
							{/if}
							{#if users_fetched}
								<div class="mt-4 space-y-4">
									<div
										class="rounded-lg border border-gray-300 bg-gray-100 p-4 transition-shadow hover:shadow-lg"
									>
										<div class="flex max-h-60 flex-col space-y-2 overflow-y-auto pr-5">
											{#if requested_users_view === 1}
												{#each requested_users as user}
													<div class="flex items-center justify-between">
														<a
															href="/user/{user.id}"
															class="text-sm text-gray-600 hover:text-blue-500 hover:underline"
															>{user.name}</a
														>
														{#if hasPermission}
															<div class="flex space-x-1">
																<button
																	class="rounded bg-yellow-500 px-2 py-1 text-xs text-white hover:bg-yellow-600"
																	on:click={() => addUser(user.id)}>Accept</button
																>
															</div>
														{/if}
													</div>
												{/each}
												{#if requested_users.length == 0}
													<p class="text-sm text-gray-600">No requests</p>
												{/if}
											{:else if requested_users_view === 0}
												<h1 class="text-lg font-bold text-gray-700">Admins</h1>
												{#each admin_users as user}
													<div class="flex items-center justify-between">
														<a
															href="/user/{user.id}"
															class="text-sm text-gray-600 hover:text-blue-500 hover:underline"
															>{user.name}</a
														>
														{#if isAadmin && user.id !== usersID}
															<div class="flex space-x-1">
																<button
																	class="rounded bg-green-500 px-2 py-1 text-xs text-white hover:bg-green-600"
																	on:click={() => demoteUser(user.id)}>Demote</button
																>
																{#if isAadmin}
																	<button
																		class="rounded bg-red-500 px-2 py-1 text-xs text-white hover:bg-red-600"
																		on:click={() => banUser(user.id)}>Ban</button
																	>
																{/if}
															</div>
														{/if}
													</div>
												{/each}
												<h1 class="text-lg font-bold text-gray-700">Moderators</h1>
												{#each moderator_users as user}
													<div class="flex items-center justify-between">
														<a
															href="/user/{user.id}"
															class="text-sm text-gray-600 hover:text-blue-500 hover:underline"
															>{user.name}</a
														>
														{#if hasPermission && user.id !== usersID}
															<div class="flex space-x-1">
																{#if isAadmin}
																	<button
																		class="rounded bg-blue-500 px-2 py-1 text-xs text-white hover:bg-blue-600"
																		on:click={() => premoteUser(user.id)}
																	>
																		Promote
																	</button>
																{/if}
																<button
																	class="rounded bg-green-500 px-2 py-1 text-xs text-white hover:bg-green-600"
																	on:click={() => demoteUser(user.id)}>Demote</button
																>
																{#if isAadmin}
																	<button
																		class="rounded bg-red-500 px-2 py-1 text-xs text-white hover:bg-red-600"
																		on:click={() => banUser(user.id)}>Ban</button
																	>
																{/if}
															</div>
														{/if}
													</div>
												{/each}
												<h1 class="text-lg font-bold text-gray-700">Users</h1>
												{#each users as user}
													<div class="flex items-center justify-between">
														<a
															href="/user/{user.id}"
															class="text-sm text-gray-600 hover:text-blue-500 hover:underline"
															>{user.name}</a
														>
														{#if hasPermission && user.id !== usersID}
															<div class="flex space-x-1">
																<div class="flex space-x-1">
																	<button
																		class="rounded bg-blue-500 px-2 py-1 text-xs text-white hover:bg-blue-600"
																		on:click={() => premoteUser(user.id)}
																	>
																		Promote
																	</button>
																	{#if isAadmin}
																		<button
																			class="rounded bg-red-500 px-2 py-1 text-xs text-white hover:bg-red-600"
																			on:click={() => banUser(user.id)}>Ban</button
																		>
																	{/if}
																</div>
															</div>
														{/if}
													</div>
												{/each}
											{:else if requested_users_view === 2}
												{#each banned_users as user}
													{#if isAadmin}
														<div class="flex items-center justify-between">
															<a
																href="/user/{user.id}"
																class="text-sm text-gray-600 hover:text-blue-500 hover:underline"
																>{user.name}</a
															>
															<div class="flex space-x-1">
																<div class="flex space-x-1">
																	<button
																		class="rounded bg-red-500 px-2 py-1 text-xs text-white hover:bg-red-600"
																		on:click={() => banUser(user.id)}
																	>
																		Unban
																	</button>
																</div>
															</div>
														</div>
													{/if}
												{/each}
												{#if banned_users.length == 0}
													<p class="text-sm text-gray-600">No banned users</p>
												{/if}
											{/if}
										</div>
									</div>
								</div>
							{/if}
						{/if}
					</div>
				{/if}
			</div>

			<div class="scrollbar-none mt-2 flex w-full justify-center overflow-y-auto px-4 md:w-1/2">
				<div class="w-full max-w-2xl">
					{#if private_community && !inCommunity}
						<div
							class="sticky top-5 mt-5 rounded-lg border-2 border-gray-300 bg-white p-4 shadow-md"
						>
							<h1 class="text-lg font-bold text-gray-700">Private Community</h1>
							<p class="mt-4 text-sm text-gray-600">
								This community is private. You need to join to see the posts.
							</p>
						</div>
					{/if}
					{#if communityFetched}
						{#if choice === 0}
							<div class="w-full">
								<Feed feedType="events" showActions={true} bind:communityID={int_communityId}>
									<Event url={'community/' + communityId + '/events'} slot="Posts" limit={30} />
								</Feed>
							</div>
						{:else if choice === 1}
							<div class="w-full">
								<Feed
									feedType="announcements"
									showActions={true}
									bind:communityID={int_communityId}
								>
									<Annoucements
										url={'community/' + communityId + '/announcements'}
										slot="Posts"
										limit={30}
									/>
								</Feed>
							</div>
						{/if}
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>
